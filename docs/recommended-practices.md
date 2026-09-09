# おすすめ: Context・Steering・MCP の使い分け

このページでは、Kiro IDE を実務で使うときのおすすめをまとめます。大切なのは、すべての情報や機能を最初から追加することではなく、目的に合うものを必要な範囲だけ使うことです。

```text
いま答えてほしいことを Context で渡す
        ↓
繰り返し守るルールを Steering に残す
        ↓
外部ツールの機能が必要なときだけ MCP を使う
        ↓
実行結果と Git Diff を人が確認する
```

## まずは役割を分ける

| 機能 | 役割 | 適している内容 | 適していない内容 |
|---|---|---|---|
| Context | 今回の質問に必要な根拠を渡す | 対象ファイル、選択したコード、実行結果、差分 | 毎回守らせたいルール |
| Steering | 繰り返し使う方針や判断基準を伝える | プロジェクトの前提、ファイル別ルール、確認手順 | 一度だけの修正内容 |
| MCP | Kiro だけでは行えない外部操作を提供する | 図の作成、外部サービスや専用ツールの操作 | Context やルールの代わり |

!!! tip "迷ったときの判断"
    1回の質問に必要なら **Context**、次回以降も守るなら **Steering**、外部ツールの操作が必要なら **MCP** を検討します。

# Context 管理のおすすめ

## 問いに必要な根拠だけを渡す

Context は、多いほど回答がよくなるとは限りません。最初に「何を確認したいか」を決め、その答えを確認できる根拠だけを渡します。

| 確認したいこと | 最初に使う Context |
|---|---|
| 特定の行や symbol の意味 | 選択範囲から **Ask Kiro** |
| 1つのファイルの仕様 | `#File` |
| 特定フォルダー内の関連ファイル | `#Folder` |
| IDE が検出した diagnostic | Problems の電球アイコンから **Ask Kiro** |
| tests や validator の結果 | `#Terminal` |
| 変更されたファイルと行 | `#Git Diff` |

おすすめの進め方:

1. 対象が分かっている場合は、選択範囲または `#File` から始める
2. 関連ファイルを探す必要がある場合だけ `#Folder` を使う
3. 回答には、根拠となる path、symbol、実行結果を示してもらう
4. 変更後は `#Terminal` と `#Git Diff` を分けて確認する

例:

```text
#File app.py #File docs/requirements.md この2ファイルだけを根拠に、仕様の不一致を表で示してください。根拠となる path と symbol を示し、まだファイルは変更しないでください。
```

## 避けたい使い方

- 質問と関係のないフォルダーや長いログをまとめて渡す
- Kiro の回答に根拠を求めず、そのまま変更を承認する
- `#Terminal` の成功だけで、意図しないファイル変更がないと判断する
- `#Git Diff` だけで、tests や validator が成功したと判断する

# Steering のおすすめ

## 適用範囲を小さく保つ

Steering には、今後も繰り返し使う内容だけを残します。ルールの適用範囲が広すぎると、関係のない作業でも読み込まれ、指示が競合しやすくなります。

| 適用方法 | おすすめの用途 | 例 |
|---|---|---|
| `always` | すべての作業で必要な少数の前提 | コードを現行仕様として扱う、変更前に根拠を確認する |
| `fileMatch` | 特定ファイルを扱うときだけ必要なルール | Python と関連ドキュメントを同期する |
| `manual` | 人が必要な場面で選ぶ確認手順 | リリース前のドキュメント確認 |
| `auto` | 内容が多く、特定の依頼に一致したときだけ必要な知識 | API 設計、migration、障害調査の手順 |

本ハンズオンでは `always`、`fileMatch`、`manual` を扱います。`auto` は、より大きなプロジェクトで必要になった場合に検討する発展的な選択肢です。

## 文章量の目安

Kiro に固定の文字数制限があるわけではありません。次は、読みやすさと Context の量を保つための実用的な目安です。日本語は単語を空白で区切らないため、文字数も併記します。

| 適用方法 | 1ファイルの目安 | 内容の目安 |
|---|---|---|
| `always` | 100〜250 words、または日本語300〜700文字 | 5〜15個の短いルール |
| `fileMatch` | 150〜400 words、または日本語450〜1,200文字 | 1つの技術・ファイル種別に関するルールと例 |
| `manual` | 200〜600 words、または日本語600〜1,800文字 | 必要なときだけ使う手順やチェックリスト |
| `auto` | 200〜600 words、または日本語600〜1,800文字 | description に一致した依頼だけで使う専門知識 |

!!! tip "分割する目安"
    1ファイルが約600 wordsまたは日本語1,800文字を超える、見出しが3つ以上の異なる領域に分かれる、同じファイル内で複数の `fileMatchPattern` が必要になる場合は、目的別に分割します。

文字数を増やすより、次の順で書くほうが効果的です。

1. **目的**: この Steering が何を防ぐのか
2. **必須ルール**: Kiro が実行できる短い指示
3. **具体例**: 推奨する例を1つ、避ける例を1つ
4. **確認方法**: tests、validator、Git Diff などの完了条件

## おすすめのフォルダー構成

最初は `.kiro/steering/` 直下へ、1つの領域につき1ファイルを置く平坦な構成がおすすめです。ファイル数が少ないうちは、階層を増やすより名前で役割が分かる状態を優先します。

```text
project-root/
├── .kiro/
│   └── steering/
│       ├── product.md
│       ├── tech.md
│       ├── structure.md
│       ├── docs-standards.md
│       ├── testing-standards.md
│       └── release-checklist.md
├── docs/
├── src/
└── tests/
```

| ファイル | 推奨する inclusion | 役割 |
|---|---|---|
| `product.md` | `always` | 製品の目的、利用者、重要な制約 |
| `tech.md` | `always` | 採用している言語、framework、主要な技術判断 |
| `structure.md` | `always` | directory、命名、依存方向の基本ルール |
| `docs-standards.md` | `fileMatch` | Markdown やドキュメントを扱うときのルール |
| `testing-standards.md` | `fileMatch` | test file を扱うときのパターンと確認方法 |
| `release-checklist.md` | `manual` | リリース前だけ選択する確認手順 |

`product.md`、`tech.md`、`structure.md` は Kiro IDE の **Generate Steering Docs** で作成できる foundation files です。生成後は内容をそのまま増やし続けず、現在のプロジェクトに必要な情報だけへ整理します。

## ファイル名と front matter

- ファイル名は小文字の kebab-case にする: `api-standards.md`
- `guide.md` や `rules.md` のような曖昧な名前を避ける
- 1ファイルにつき1つの領域にする
- front matter はファイルの先頭に置き、その前に空行や文章を入れない
- `fileMatchPattern` は project root から見た glob として書く
- 認証情報、秘密情報、個人情報を含めない

`fileMatch` の例:

```markdown
---
inclusion: fileMatch
fileMatchPattern: ["docs/**/*.md", "README.md"]
---

# Documentation standards

- Treat source code as the current behavioral source of truth.
- Update only documentation supported by code, tests, or validator output.
- Run the documentation validator before reporting completion.
```

`manual` の例:

```markdown
---
inclusion: manual
---

# Release documentation review

- Review user-visible behavior changed in this release.
- Confirm commands and examples match the current code.
- Ask for human review before publishing externally.
```

## 長い情報は参照する

仕様書や設定内容を Steering へコピーすると、元ファイルとのずれが発生します。既存ファイルを根拠として使う場合は、Kiro の file reference を利用できます。

```markdown
#[[file:docs/api-spec.md]]
#[[file:pyproject.toml]]
```

参照先を変更・移動した場合は link も更新します。大きなファイルを無条件に参照すると Context が増えるため、`fileMatch`、`manual`、`auto` と組み合わせます。

## 作成・更新時の小さな確認

Steering に残す前に、次を確認します。

- 次回の別作業でも使うルールか
- 適用対象を `fileMatch` で絞れないか
- 1つの bullet に1つの指示だけが書かれているか
- 「適切に」「必要に応じて」ではなく、実行できる条件になっているか
- 推奨例と避ける例が現在のコードに合っているか
- 既存の Steering と矛盾していないか
- 一度直せば終わる内容を混ぜていないか
- 完了を tests、validator、lint、Git Diff のどれで確認するか明確か

Steering の変更もコード変更と同様に review 対象にします。構成変更、framework 更新、リリース手順変更のタイミングで見直し、使われなくなったルールは削除します。

## Steering にしないほうがよい内容

- 今回だけ変更するファイル名や値
- 一時的な調査メモ
- 実行のたびに変わる Terminal output
- validator で機械的に確認できる結果そのもの
- 外部サービスへの接続情報や認証情報

# MCP のおすすめ

## 必要な機能だけを接続する

MCP server は、Kiro に新しい操作機能を追加します。便利ですが、server ごとに tool、権限、送信データ、障害時の影響が増えます。使用する作業が決まってから、必要な server だけを有効にします。

MCP を追加する前の確認項目:

1. Kiro の標準機能だけでは実行できない作業か
2. どの server と tool が呼び出されるか
3. どのデータが server へ送られるか
4. 読み取りと書き込みのどちらが必要か
5. 失敗した場合の手動手順があるか
6. 作業後も有効にしておく必要があるか

MCP tool の承認画面では、server 名、tool 名、入力内容を確認します。初めて使う tool は、可能であれば1回限りの許可から始めます。

!!! warning "機密情報を送らない"
    公開または外部で動作する MCP server には、個人情報、認証情報、顧客データ、非公開の構成情報を送らないでください。利用前に、組織のルールと server のデータ取扱いを確認します。

## hosted と local の選び方

| 観点 | Hosted MCP | Local MCP |
|---|---|---|
| 開始しやすさ | URL 設定だけで始められる場合がある | runtime や package の準備が必要 |
| データの流れ | request が hosted server へ送られる | local process で処理できる場合がある |
| 運用 | server 側の更新を利用できる | package version と runtime を自分で管理する |
| 障害時 | network や server availability の影響を受ける | local runtime や process 起動の影響を受ける |

どちらが常に優れているわけではありません。データの取扱い、セットアップの容易さ、必要な tool、運用責任を比較して選びます。

# 3つを組み合わせるおすすめの流れ

```text
1. 目的を1文で決める
2. Context で根拠を絞る
3. Kiro に変更案と根拠を出してもらう
4. 人が変更範囲と権限を確認する
5. 必要な場合だけ MCP tool を実行する
6. tests / validator と Git Diff で確認する
7. 繰り返すルールだけ Steering に残す
```

例として、コードから構成図を作る場合は次のように分けます。

| 段階 | 使用するもの | 目的 |
|---|---|---|
| 根拠を渡す | `#File` | 実装に存在する要素と flow を確認する |
| 作成ルールを伝える | Steering または今回の prompt | 推測した要素を追加しない |
| 図を作成する | draw.io MCP | 編集可能な図を生成する |
| 結果を確認する | `#Git Diff` と人のレビュー | コード、図、ドキュメントの整合性を確認する |

# 実務へ持ち帰るチェックリスト

- [ ] 質問の目的を1文で説明できる
- [ ] Context を必要な path、symbol、output に絞った
- [ ] Kiro の回答に確認できる根拠がある
- [ ] Steering は繰り返し使うルールだけになっている
- [ ] Steering の適用範囲が必要以上に広くない
- [ ] MCP server、tool、権限、送信データを確認した
- [ ] MCP が使えない場合の手動手順がある
- [ ] tests / validator と Git Diff の両方を確認した
- [ ] 最終判断を人が行った

## 参考資料

- [Kiro Steering](https://kiro.dev/docs/steering/)
- [Kiro MCP](https://kiro.dev/docs/mcp/)
- [Kiro Agent Hooks](https://kiro.dev/docs/hooks/)
