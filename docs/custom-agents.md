# おすすめ: Custom Agent の考え方と使い方

このページでは、Kiro IDE 1.x の **Custom Agent** を、いつ・なぜ・どう使うかをまとめます。Steering が「Kiro に守らせるルール」なら、Custom Agent は「その仕事のために Kiro が使える道具と権限を決めたプロファイル」です。

```text
毎回同じ指示を繰り返している        → Steering
特定の作業だけ道具と権限を絞りたい    → Custom Agent
実装と審査を別々の agent に分けたい   → Custom Agent + Sub-agent
```

!!! info "情報の出典"
    このページは [Kiro 公式ドキュメント（Custom agents）](https://kiro.dev/docs/custom-agents/)、[Configuration reference](https://kiro.dev/docs/custom-agents/configuration-reference/)、[Invoking as sub-agents](https://kiro.dev/docs/custom-agents/subagents/) を基にしています。仕様は変わることがあるため、迷ったら公式ドキュメントを優先してください。

# Custom Agent とは

## 1 ファイル = 1 つの役割

Custom Agent は、`.kiro/agents/` に置く 1 つの設定ファイルです。次を決めます。

| 決めること | フィールド | 例 |
|---|---|---|
| 何ができるか | `tools` | `read` だけ、`read` + `shell` など |
| 何を確認なしに実行してよいか / 何を禁止するか | `permissions.rules` | `terraform validate*` は allow、`terraform apply*` は deny |
| 最初から読んでおく資料 | `resources` | Steering ファイル、README、Skill |
| 振る舞いの前提 | `prompt` | 「審査だけを行い、ファイルは編集しない」 |
| 使う model（任意） | `model` | 省略すると IDE の既定 model |
| 表示名と説明 | `name`, `description` | Sub-agent の自動選択にも使われる |

## Steering との違い

| | Steering | Custom Agent |
|---|---|---|
| 変えるもの | **考え方・判断基準**（何を守るか） | **道具と権限**（何ができるか） |
| 適用範囲 | 常に、またはファイル種別ごと | その agent を選んだとき、または sub-agent として呼ばれたとき |
| 典型例 | 命名規則、確認手順、禁止事項 | read-only の reviewer、apply を禁止した implementer |
| 組み合わせ | — | `resources` に Steering を指定して両方使う |

!!! tip "迷ったら"
    「Kiro にどう考えてほしいか」なら Steering、「Kiro に何をさせない（させる）か」なら Custom Agent。多くの場合、**Steering をまず書き、その Steering を読む Custom Agent を後から足す**のが自然です。

## 置き場所

| 場所 | 用途 | 共有 |
|---|---|---|
| `.kiro/agents/<name>.json`（または `.md`） | プロジェクト専用 | Git で team に共有される。workspace を trust したときだけ読み込まれる |
| `~/.kiro/agents/<name>.json` | 自分の全プロジェクト共通 | 個人用 |

同名がある場合はプロジェクト側が優先されます。JSON と Markdown の 2 形式があり、長い `prompt` を書くなら Markdown（front matter に設定、本文が prompt）が読みやすいです。

## IDE でできること

| 機能 | IDE | CLI | Web |
|---|---|---|---|
| プロジェクト agent（`.kiro/agents/`） | ○ | ○ | ○ |
| グローバル agent（`~/.kiro/agents/`） | ○ | ○ | — |
| UI で agent を切り替える | ○ | ○ | — |
| Sub-agent として呼び出す | ○ | ○ | ○ |

# 最小の例

`.kiro/agents/reviewer.json` — ファイルを**書けない**審査役です。

```json
{
  "name": "reviewer",
  "description": "Read-only reviewer. Checks diffs against project standards and ends with APPROVED or NEEDS_CHANGES.",
  "tools": ["read", "shell"],
  "permissions": {
    "rules": [
      { "capability": "shell", "match": ["git diff*", "git status*"], "effect": "allow" }
    ]
  },
  "resources": ["file://.kiro/steering/project-standards.md"],
  "prompt": "Review the current Git Diff against the standards. List required changes as bullets and end with NEEDS_CHANGES, otherwise end with APPROVED. Never edit files."
}
```

ポイント:

- `tools` に `write` が無いので、prompt に何を書いても**ファイルは変更できない**。役割の分離は文章ではなく設定で保証する
- `permissions.rules` は `allow`（確認なしで実行）/ `ask`（確認する）/ `deny`（常に拒否）。`deny` は他の scope の `allow` より常に優先される
- `resources` の `file://` は workspace root からの相対パス。Steering を `fileMatch` にしていても、ここで指定すれば agent は必ず読む

# 使い方 1: 作業別の primary agent として切り替える

チャットの agent 選択 UI で Custom Agent を選ぶと、その会話全体がその agent の道具と権限で動きます。

向いている場面:

- **調査専用**: `tools: ["read", "shell"]`、shell は `grep*` / `git log*` / `terraform plan*` などの読み取り系だけ allow。誤って修正しない
- **ドキュメント整備専用**: `write` は許すが `permissions` で `fs_write` を `docs/**` に限定
- **IaC 変更専用**: `terraform fmt*` / `validate*` は allow、`apply*` / `destroy*` / `import*` / `state*` は deny

```json
{
  "name": "docs-writer",
  "description": "Updates documentation under docs/ only.",
  "tools": ["read", "write", "shell"],
  "permissions": {
    "rules": [
      { "capability": "fs_write", "match": ["docs/**"], "effect": "allow" },
      { "capability": "fs_write", "match": ["**"], "effect": "ask" },
      { "capability": "shell", "match": ["mkdocs build*", "git diff*"], "effect": "allow" }
    ]
  },
  "resources": ["file://.kiro/steering/docs-standards.md"],
  "prompt": "Edit only files under docs/. Run mkdocs build --strict after changes and show the Git Diff."
}
```

`keyboardShortcut`（例 `"ctrl+r"`）を付けると、切り替えがワンキーになります。

# 使い方 2: 実装役と審査役を分ける（Sub-agent）

Custom Agent は、メインの会話から **Sub-agent** として呼び出せます。Sub-agent は自分専用の context window で動き、終わったら結果だけをメインに返します。

チャットでの依頼例:

```text
implementer agent を使って main.tf の log group に標準タグを追加し、
reviewer agent に diff を審査させてください。
APPROVED が出るまで implementer に差し戻し、最大 3 回までにしてください。
apply は実行しないでください。
```

Kiro は次のような pipeline を組みます。

```text
implementer ──diff──▶ reviewer ──NEEDS_CHANGES──▶ implementer（再実行）
                          └──APPROVED──▶ 完了
```

Review loop の仕組み:

| 要素 | 意味 |
|---|---|
| target | 差し戻し先の stage（implementer） |
| trigger | 差し戻しを起こす出力文字列（`NEEDS_CHANGES`、4 文字以上） |
| max_iterations | 上限回数（1〜10） |

制約: stage は自分自身には戻れない、A→B→A の相互ループは不可、task graph は開始前に固定される（途中で変更できない）。

## Sub-agent が引き継ぐもの / 引き継がないもの

| メインと共有 | Sub-agent ごとに独立 |
|---|---|
| Steering | 会話履歴 |
| MCP server | context window |
| workspace のファイル | Spec の状態 |
| Permissions 設定 | Hook の発火 |

**会話履歴を共有しない**のが重要です。reviewer は implementer の「言い分」を見ず、diff と Steering だけで判断します。人間のコードレビューと同じ構図です。

## 並列実行

独立した作業は同時に走ります。

```text
3 つの service を新しい auth middleware に移行してください。並列で進めてください。
```

依存関係がある場合は Kiro が DAG を組み、独立した stage だけ並列にします。

# 使い方 3: team で共有する

`.kiro/agents/` を Git に入れると、team 全員が同じ道具・権限・前提で Kiro を使えます。

おすすめの運用:

1. Steering を先に整える（`project-standards.md` など）
2. その Steering を `resources` に持つ agent を 1〜2 個だけ作る（まず reviewer）
3. PR で agent 設定を review する。特に `permissions` の `allow` 一覧
4. 「この agent を使ってください」を README や PR template に書く
5. 増やす前に、既存 agent の `description` を見直す（Sub-agent の自動選択はこの文で決まる）

!!! warning "agent 設定ファイルも Kiro が書ける"
    `write` を持つ agent は `.kiro/agents/` や `~/.kiro/` の中も編集できます。agent 設定の変更は Git Diff で人が確認してください。

# 使い方 4: Skill・MCP・model を役割ごとに絞る

## Skill を `resources` で渡す

```json
"resources": [
  "file://.kiro/steering/**/*.md",
  "skill://.kiro/skills/**/SKILL.md"
]
```

`file://` は起動時に全文を読み込み、`skill://` は名前と説明だけ先に読み、必要になったとき本文を読みます。長い手順書は Skill にすると context を節約できます。

## MCP を agent 単位で絞る

`tools` に `@server名` や `@server名/tool名` を書けば、その agent だけが使える MCP tool を限定できます。`includeMcpJson: false` にすると workspace の `mcp.json` を読み込まず、`mcpServers` に書いたものだけ使います。

```json
"tools": ["read", "shell", "@aws-knowledge/search_documentation", "@aws-knowledge/read_documentation"],
"includeMcpJson": false
```

## model を役割ごとに変える

```json
"model": "claude-sonnet-5"
```

実装役は速い model、審査役は見落としの少ない model、というように分けられます。ID はチャットの `/model` で確認できます。指定した model が使えない場合は既定 model に fallback して warning が出るだけで、pipeline は止まりません。会社の model governance がある場合は `model` を書かず既定に任せます。

# 安全に使うためのチェック

- [ ] `tools` は必要最小限か（`*` や `@builtin` を安易に使っていない）
- [ ] `write` を持つ agent は `permissions` で書き込み範囲を限定しているか
- [ ] `shell` の `allow` に破壊的な command（apply / destroy / rm -rf / sudo / delete 系）が無いか
- [ ] reviewer など「判断役」は `write` を持っていないか
- [ ] `resources` に credential や顧客データを含むファイルを渡していないか
- [ ] `description` を読めば、Kiro が正しく自動選択できるか
- [ ] agent 設定の変更は Git Diff で人が確認しているか

# 避けたい使い方

| やりがちなこと | 問題 | 代わりに |
|---|---|---|
| prompt に「ファイルを編集しないで」と書くだけ | prompt は破られることがある | `tools` から `write` を外す |
| 1 つの agent に全部の役割を詰める | 権限が最大公約数になり、分ける意味が消える | 役割ごとに agent を分け、Sub-agent で組み合わせる |
| `tools: ["*"]` + `allowedTools` で全部許可 | 確認なしで何でも実行できる | 必要な tool と command だけ allow |
| Steering の内容を agent の prompt にコピーする | 二重管理になりズレる | Steering を `resources` で参照する |
| agent を大量に作る | どれを使うか誰も分からない | まず reviewer 1 つから。増やすときは `description` を明確に |

# 1 つだけ試すなら

1. いま使っている Steering を 1 つ選ぶ
2. それを `resources` に持つ **read-only の reviewer** を `.kiro/agents/reviewer.json` に作る
3. 自分が普通に修正したあと、チャットで「reviewer agent で diff を審査してください」と頼む
4. 指摘が妥当かを自分の目で確認する

これが回るようになったら、implementer を足して review loop にします。

## 参考

- [Kiro Docs: Custom agents](https://kiro.dev/docs/custom-agents/)
- [Kiro Docs: Configuration reference](https://kiro.dev/docs/custom-agents/configuration-reference/)
- [Kiro Docs: Invoking as sub-agents](https://kiro.dev/docs/custom-agents/subagents/)
- [Kiro Docs: Permissions](https://kiro.dev/docs/permissions/)
- [Kiro Docs: Steering](https://kiro.dev/docs/steering/)
