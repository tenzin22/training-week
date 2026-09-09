# 参加者ガイド: 開発中のコードに合わせてドキュメントを整備する

## ゴール

`app.py` を現行仕様として、必要な Context だけでドキュメントのずれを直し、Steering と Hook で再発を防ぎます。

## 題材のアプリを理解する

この演習で使うのは、架空の求人情報を表示する小さなコマンドラインアプリです。求人情報は `data/jobs.json` に保存され、`app.py` がその内容を読み取って画面へ表示します。

たとえば、募集中の求人だけを確認したい場合に `--status open` を指定します。

```text
利用者
  │
  │ python3 app.py --status open
  ▼
app.py（Job List CLI）
  │
  │ data/jobs.json を読み込む
  ▼
status が open の求人だけを表示
```

### 入力例

Windows:

```powershell
py -3.12 app.py --status open
```

macOS / Linux:

```bash
python3 app.py --status open
```

### 出力例

```text
JOB-001    一般事務    東京    open
JOB-003    ITサポート  大阪    open
```

このアプリのコードは正しく動きますが、要件、保存形式、CLI option を説明するドキュメントには古い記載が残っています。演習ではアプリのコードを変更せず、Kiro へ適切な根拠を渡してドキュメントを現行仕様へ合わせます。

## タイムテーブル

| 内容 |
|---|
| 講義 | 
| Starter Project | 
| Context deep dive |
| Steering |
| Agent Hooks |
| 休憩 |
| draw.io |
| Checkpoints |
| Q&A・振り返り |

各章で「予測する -> 実行する -> 結果を見る -> 次回も効く仕組みにする」を繰り返します。

# 1. Starter Project

> **この章が役立つ場面:** 作業前に、アプリケーションと検証環境が期待どおり動くか確認したいとき。
>
> **この章を終えると:** コードは正常で、ドキュメントだけに3件のずれがある開始状態を説明できるようになります。

Kiro IDE で `starter-project` を開きます。

### Windows PowerShell

```powershell
py -3.12 --version
py -3.12 -m unittest discover -s tests -v
py -3.12 scripts/validate_docs.py
py -3.12 app.py
```

### macOS /

```bash
python3 --version
python3 -m unittest discover -s tests -v
python3 scripts/validate_docs.py
python3 app.py
```

### Linux

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

開始状態ではテスト3件が成功し、validator は次の3件を報告します。

```text
コード: status は open / closed    ドキュメント: open / paused
コード: JSON                       ドキュメント: CSV
コード: --status                   ドキュメント: --state
```

この時点ではファイルを変更しません。

## Git baseline

Checkpoint 自体は Git 不要ですが、`#Git Diff` のため参加者本人が初期 commit を作ります。

```bash
git init -b main
git config user.name "Kiro Workshop Participant"
git config user.email "kiro-workshop@example.invalid"
git add .
git commit -m "chore: establish workshop baseline"
git status --short
```

`git status --short` に何も表示されれば合格です。

## 1.1 画面配置

1. Kiro のチャットタブを右クリックします。
2. **Open in Editor** を選び、Dockable Chat をコードやドキュメントの横へ配置します。
3. 利用できない場合は通常のチャットパネルのまま続けます。

# 2. Context: AI に渡す情報を最適化する

> **この章が役立つ場面:** Kiro の回答に不要な情報が多い、根拠が分からない、実行結果とファイル変更が混ざっているとき。
>
> **この章を終えると:** 問いに応じて、選択範囲、`#File`、`#Folder`、Problems、`#Terminal`、`#Git Diff` を選び、確認できる根拠を Kiro へ渡せるようになります。

## 2.1 Context の特徴を理解する

Context は、多ければ多いほどよいわけではありません。まず、それぞれが何を根拠として渡す機能なのかを確認します。

| Context | 役立つ場面 | 渡せる根拠 |
|---|---|---|
| 選択範囲から Ask Kiro | 調べたい行や symbol が分かっている | 選択したコードや文章 |
| `#File` | 対象ファイルが分かっている | そのファイルの内容 |
| `#Folder` | 特定フォルダー内を横断して確認したい | フォルダー内の複数ファイル |
| Problems の **Ask Kiro** | IDE が検出した syntax・type・import error を調べたい | 選択した diagnostic |
| `#Terminal` | tests や validator の実行結果を確認したい | 選択した Terminal output |
| `#Git Diff` | 変更されたファイルと行を確認したい | Git の差分 |

Problems はチャットへ `#Problems` と入力する操作ではありません。Problems タブで対象の問題を選び、電球アイコンをクリックして **Ask Kiro** を選ぶと、その diagnostic が Kiro へ送られます。

## 2.2 Context 選択クイズ

説明を確認した後で、各場面に最初に使う Context を選びます。

| 場面 | 自分の選択 | 推奨 |
|---|---|---|
| `app.py` の `ALLOWED_STATUSES` を確認したい |  | 選択範囲 / `#File` |
| `docs/` 全体の記載を横断して確認したい |  | `#Folder` |
| IDE が表示した syntax error の原因を調べたい |  | Problems の **Ask Kiro** |
| tests / validator の実行結果を根拠にしたい |  | `#Terminal` |
| 適用後に何が変わったか確認したい |  | `#Git Diff` |

## 2.3 選択範囲と `#File` で status のずれを確認する

最初に `app.py` の `ALLOWED_STATUSES` を選択し、Windows / Linux は `Ctrl+L`、macOS は `Cmd+L` で Ask Kiro へ追加します。

```text
選択したコードだけを根拠に、このアプリが対応する status を説明してください。根拠となる symbol を示し、ファイルは変更しないでください。
```

次に、コードとドキュメントを一緒に渡します。

```text
#File app.py #File docs/requirements.md この2ファイルだけを根拠として、status の不一致を表で示してください。コードを現行仕様として扱い、まだ変更しないでください。
```

期待結果: `paused` はドキュメントだけ、`closed` はコードだけにあります。

この比較から、コードだけでは実装の事実を確認できても、ドキュメントとのずれまでは判断できないことを確認します。

## 2.4 必要な箇所に絞って修正する

保存形式と CLI option も含め、修正が必要な箇所だけを確認します。

```text
#File app.py #File data/jobs.json #Folder docs/ #File scripts/validate_docs.py コードとデータを現行仕様として、status、storage_format、filter_option の不一致を示してください。app.py、data、tests は変更せず、ドキュメントで修正が必要な箇所だけを提案してください。
```

提案内容を確認してから、次を送ります。

```text
承認した3箇所だけをドキュメントへ反映してください。app.py、data、tests、CHANGELOG は変更しないでください。
```

修正後に実行します。

### Windows PowerShell

```powershell
py -3.12 -m unittest discover -s tests -v
py -3.12 scripts/validate_docs.py
py -3.12 app.py --status open
```

### macOS / Linux

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_docs.py
python3 app.py --status open
```

## 2.5 `#Terminal` と `#Git Diff`: 実行結果と変更結果を分ける

```text
#Terminal #Git Diff tests と validator の実行結果、変更されたファイル、docs 以外の意図しない変更の有無を報告してください。各結論に Terminal または Git Diff の根拠を付け、ファイルは変更しないでください。
```

確認する違い:

```text
#Terminal -> 実際に何が実行され、成功・失敗したか
#Git Diff -> どのファイルのどの行が変わったか
```

`#Terminal` に長いログ全体を渡す必要はありません。今回の tests と validator の結果だけを選びます。

## 2.6 Problems から diagnostic を Ask Kiro へ送る（任意）

Python diagnostics が利用できる環境だけで実施します。

1. project root に一時ファイル `context_problem_demo.py` を作る
2. 次の1行を保存する

```python
if True print("demo")
```

3. Kiro IDE の **Problems** タブを開く
4. 表示された syntax error を選択する
5. 問題の横にある電球アイコンをクリックする
6. **Ask Kiro** を選ぶ
7. Kiro Chat で次を送る

```text
この問題の原因と、必要な修正だけを説明してください。まだファイルは変更しないでください。
```

確認後、`context_problem_demo.py` を削除し、`git status --short` が clean であることを確認します。

Problems が表示されない場合は深追いせず、講師画面で操作方法だけを確認します。Problems はドキュメントの意味のずれではなく、IDE が検出した diagnostic を Kiro へ渡すために使います。

## Context の持ち帰り

```text
問いに必要な情報を選ぶ
        |
対象が分かったらファイルや選択範囲へ絞る
        |
実行結果と差分を別々に確認する
        |
path / symbol / output で確認できる回答にする
```

# 3. Steering: 再利用するルールを設計する

> **この章が役立つ場面:** 同じ注意事項を毎回 Kiro に伝えている、ファイルによって必要なルールが違う、リリース前だけ確認したい項目があるとき。
>
> **この章を終えると:** ルールを `always`、`fileMatch`、`manual` に分け、今回だけの修正を Steering に残さない判断ができるようになります。

## 3.1 3種類の適用方法を理解する

| 適用方法 | 使う場面 | この演習の例 |
|---|---|---|
| `always` | すべての作業で必要な前提 | 合成データだけを使う、完了前に検証する |
| `fileMatch` | 特定ファイルを扱うときだけ必要 | `app.py` を変更したら関連ドキュメントを確認する |
| `manual` | 人が必要な節目で明示して使う | リリース前の確認 |

`paused` を `closed` に直す、CSV の記載を JSON に直す、といった一度直せば終わる内容は Steering に残しません。

## 3.2 always: プロジェクト全体の前提

`.kiro/steering/project-context.md`

```markdown
---
inclusion: always
---

# プロジェクトの前提

- 対象は架空の Synthetic Job List CLI である。
- Python 3.12 と標準ライブラリだけを使用する。
- 実在の候補者、顧客、個人情報、認証情報、社内リソース ID を追加しない。
- ドキュメントの記載には `app.py`、tests、validator の根拠を付ける。
- 完了前に tests と `scripts/validate_docs.py` を実行する。
- 自動 commit、外部送信、依存関係の追加は行わない。
```

## 3.3 fileMatch: `app.py` を扱うときだけ

`.kiro/steering/python-doc-sync.md`

```markdown
---
inclusion: fileMatch
fileMatchPattern: "app.py"
---

# コードとドキュメントの同期

- status を変更したら `docs/requirements.md` を確認する。
- データ形式または保存先を変更したら `docs/architecture.md` を確認する。
- CLI option を変更したら `docs/operations.md` を確認する。
- 推測した外部サービスを追加しない。
```

## 3.4 manual: リリース前に明示して使う

`.kiro/steering/release-doc-review.md`

```markdown
---
inclusion: manual
---

# リリース前のドキュメント確認

- [ ] tests が成功
- [ ] `scripts/validate_docs.py` が成功
- [ ] Git Diff に意図しない app、test、data の変更がない
- [ ] 実在の人物、顧客、秘密情報がない
- [ ] `CHANGELOG.md` の Unreleased が更新済み
- [ ] `docs/architecture.drawio` が開ける
```

## 3.5 分類クイズ

説明と template を確認した後で、次の rule を分類します。

| Rule | 自分の分類 |
|---|---|
| 架空のデータだけを使う |  |
| コードを現行仕様として扱う |  |
| `app.py` の status・保存形式・option を変えたら docs を確認する |  |
| リリース前に tests、validator、Git Diff、CHANGELOG を確認する |  |
| `paused` を `closed` へ修正する |  |
| CSV の記載を JSON へ修正する |  |
| 推測した外部サービスを追加しない |  |

### 答え合わせ

| 分類 | Rule |
|---|---|
| `always` | 架空データ、コードを現行仕様とする、推測サービスを追加しない |
| `fileMatch` | `app.py` の status・保存形式・option 変更時に関連 docs を確認 |
| `manual` | release 前の tests、validator、Git Diff、CHANGELOG、図 |
| Steering に置かない | `paused -> closed`、`CSV -> JSON` |

## 3.6 Steering の適用を確認する

まず、manual Steering を選択せずに次を送ります。

```text
現在有効な Steering を always・fileMatch・manual に分けて説明してください。manual の release-doc-review はまだ適用しないでください。app.py を変更する依頼と docs/operations.md だけを変更する依頼で、どの Steering が適用されるか比較してください。ファイルは変更しないでください。
```

次に manual Steering を明示します。

```text
#release-doc-review を適用して、今回の変更がリリース可能か確認してください。tests、validator、Git Diff、機密情報、CHANGELOG、architecture.drawio を Pass / Fail で報告してください。ファイルは変更しないでください。
```

`CHANGELOG.md` が未更新なら Fail または要対応になることを確認し、Unreleased に次を1行追加します。

```markdown
- 開発中のドキュメントを現行実装へ同期。
```

# 4. Agent Hook: 何を自動化するか決める

> **この章が役立つ場面:** 同じ検証を毎回手で実行している、またはドキュメントのずれを見逃したくないとき。
>
> **この章を終えると:** 自動化できる客観的な検査と、人が判断すべき内容を分け、編集後に validator を実行できるようになります。

## 4.1 自動化するものと、人が判断するものを分ける

次の表で、自動化の境界を確認します。

| 候補 | この演習での扱い | 理由 |
|---|---|---|
| docs 編集後に validator を実行 | command Hook で自動実行 | 同じ入力に同じ判定を返せる |
| CHANGELOG の文章を作成・追記 | 人が確認して判断 | 変更の価値や表現を判断する必要がある |
| 読みやすさや意味を評価 | 人が review | 機械的な合否にできない |
| formatter / lint を実行 | project に tool があれば command Hook | 結果を機械的に判定できる |
| 外部システムへ publish | 本演習では自動化しない | 権限、承認、失敗時の影響を別途設計する必要がある |

「本演習では自動化しない」は Hook の種類ではありません。外部への書き込みは、実行できるかではなく、権限、承認、再実行、失敗時の復旧まで設計してから自動化します。

この演習では、客観的な3つの contract を検査する validator だけを Hook で自動実行します。

## 4.2 Kiro に validator Hook の作成を依頼する

Kiro IDE の **Agent Hooks** で **+** を選び、**Ask Kiro to create a hook** を開きます。OS に合う prompt を Kiro Chat へ送ります。

### Windows

```text
v1 Agent Hook を1つ作成してください。

要件:
- 保存先は `.kiro/hooks/validate-docs.json`
- Hook 名は `validate-docs`
- trigger は `PostFileSave`
- action type は `command`
- command は `py -3.12 scripts/validate_docs.py`
- matcher は `docs[\\\\/].*\\.md$`
- 他の Hook、Steering、アプリケーションコードは変更しない

最初に作成予定の JSON 全体を表示してください。まだファイルには書き込まないでください。
```

### macOS / Linux

```text
v1 Agent Hook を1つ作成してください。

要件:
- 保存先は `.kiro/hooks/validate-docs.json`
- Hook 名は `validate-docs`
- trigger は `PostFileSave`
- action type は `command`
- command は `python3 scripts/validate_docs.py`
- matcher は `docs[\\\\/].*\\.md$`
- 他の Hook、Steering、アプリケーションコードは変更しない

最初に作成予定の JSON 全体を表示してください。まだファイルには書き込まないでください。
```

Kiro が表示した JSON で、次の項目を確認します。

| 項目 | Windows | macOS / Linux |
|---|---|---|
| `version` | `v1` | `v1` |
| `name` | `validate-docs` | `validate-docs` |
| `trigger` | `PostFileSave` | `PostFileSave` |
| `action.type` | `command` | `command` |
| `action.command` | `py -3.12 scripts/validate_docs.py` | `python3 scripts/validate_docs.py` |
| `matcher` | `docs[\\\\/].*\\.md$` | `docs[\\\\/].*\\.md$` |

内容に問題がなければ、次を送ります。

```text
確認した JSON を `.kiro/hooks/validate-docs.json` に保存してください。他のファイルは変更しないでください。
```

Kiro の権限設定により `.kiro/hooks/` への書き込みが拒否された場合は、Kiro が表示した JSON を使って参加者が `validate-docs.json` を手動で作成します。権限を迂回するよう Kiro に依頼しません。

### Hook の読み込みを確認する

1. Kiro IDE の **Agent Hooks** パネル、または Command Palette の **Open Kiro Hook UI** を開く
2. `validate-docs` が表示され、有効で、schema error がないことを確認する
3. 表示されない場合は Hooks UI を Refresh / Reload する
4. それでも表示されない場合は Kiro IDE を完全に終了して起動し直す
5. Terminal で validator を1回実行し、command 単体が成功することを確認する

Windows:

```powershell
py -3.12 scripts/validate_docs.py
```

macOS / Linux:

```bash
python3 scripts/validate_docs.py
```

`validate_docs.py` は成功・失敗のメッセージを標準エラー出力（stderr）へ書き出します。終了コードは、成功時が `0`、ドキュメントの不一致がある場合は `1` です。`Documentation validation passed.` が表示されてから次へ進みます。

??? info "発展: 自然言語の agent action（本ハンズオンの対象外）"
    `action.type` を `agent` にすると、command の代わりに自然言語 prompt を Agent へ渡せます。ただし、終了コードで検証結果を直接確認できる command Hook の方が、この演習には適しています。

    ```json
    {
      "version": "v1",
      "hooks": [
        {
          "name": "ask-agent-to-validate-docs",
          "trigger": "PostFileSave",
          "action": {
            "type": "agent",
            "prompt": "ドキュメント変更後に scripts/validate_docs.py を実行し、結果を報告してください。ファイルは変更しないでください。"
          }
        }
      ]
    }
    ```

??? info "発展: Agent の応答終了時に validator を確認して実行する（任意）"
    `confirm` を使うと、command を実行する前に質問と選択肢を表示できます。公式 v1 schema では、`confirm` を利用できるのは `Stop` trigger の command Hook だけです。`PostFileSave` の validator Hook へは追加できません。

    starter project では、Agent が応答を終えたときに validator を実行するか参加者へ確認する Hook として利用できます。Windows の例を `.kiro/hooks/confirm-final-validation.json` に保存する場合は次のようになります。

    ```json
    {
      "version": "v1",
      "hooks": [
        {
          "name": "Confirm final documentation validation",
          "trigger": "Stop",
          "action": {
            "type": "command",
            "command": "py -3.12 scripts/validate_docs.py"
          },
          "confirm": {
            "question": "ドキュメント validator を実行しますか？",
            "options": [
              { "id": "validate", "label": "実行する", "run": true },
              { "id": "skip", "label": "今回は実行しない", "run": false }
            ]
          }
        }
      ]
    }
    ```

    macOS / Linux では command だけを次へ置き換えます。

    ```json
    "command": "python3 scripts/validate_docs.py"
    ```

    `実行する` を選ぶと validator が実行され、`今回は実行しない` を選ぶとその回は実行されません。`Stop` は session を閉じたときではなく、Agent が応答を終えたときに発火します。そのため、この確認は複数回表示される可能性があります。

    本ハンズオンの中心は、ドキュメント変更時に自動実行する `PostFileSave` Hook です。この `Stop` Hook は、確認付き Hook の動きを試したい参加者向けの任意設定です。

## 4.3 success -> failure -> recovery を観察する

Hook の失敗確認で変更する1行:

```markdown
- `storage_format`: `json`
```

一時的な誤変更:

```markdown
- `storage_format`: `csv`
```

次を Kiro Chat へ送り、Hook の失敗を確認します。

```text
Hook の動作確認です。docs/architecture.md の `storage_format` の値だけを `json` から `csv` へ変更してください。変更するのはその1行だけです。data/jobs.json、app.py、tests、他の記述は変更しないでください。
```

`PostFileSave` Hook では `confirm` を使えないため、実行前の確認画面は表示されません。この演習では、Hook output に `Documentation validation found ...` または `Documentation validation passed.` が表示されることを、validator が実行された証拠として確認します。何も表示されない場合は Hook が発火したと見なしません。Terminal で validator を実行して誤変更を確認した後、4.2 の Hooks UI 読み込み確認へ戻ります。

Windows:

```powershell
py -3.12 scripts/validate_docs.py
```

macOS / Linux:

```bash
python3 scripts/validate_docs.py
```

失敗を確認したら、次を Kiro Chat へ送ります。

```text
docs/architecture.md の `storage_format` の値だけを `csv` から `json` へ戻してください。他のファイルや行は変更しないでください。
```

再び Hook と validator が成功することを確認します。`data/jobs.json` のファイル名は変更しません。人が手動保存しただけでは `PostFileSave` は発火しません。

> この Hook 演習の recovery は、上の2つ目の prompt で1行を戻す操作です。ここでは Checkpoint Restore を使いません。Checkpoint は Section 6 で、完成状態を commit してから別に演習します。Hook が未読込のままでも Checkpoint が代わりに実行されるわけではありません。

# 5. draw.io

> **この章が役立つ場面:** コードから構成図を作り、実装と図のずれを防ぎたいとき。
>
> **この章を終えると:** 根拠のある3要素・3フローの編集可能な図を作り、ドキュメントから参照できるようになります。

[draw.io 統合ラボ](drawio-lab.md) に従い、3要素の編集可能な図を作ります。

```text
User -- --status --> Job List CLI -- read --> data/jobs.json
                         |
                         +-- tab-separated result --> User
```

# 6. Checkpoints

> **この章が役立つ場面:** Agent の変更が意図と違ったときに、安全に直前の状態へ戻したいとき。
>
> **この章を終えると:** Git と Checkpoint の役割を区別し、1件の誤変更を Restore して検証できるようになります。

完成状態を参加者本人が commit します。

```bash
git add .
git commit -m "docs: complete workshop exercises"
git status --short
```

Checkpoint で変更する1行:

```markdown
- `filter_option`: `--status`
```

一時的な誤変更:

```markdown
- `filter_option`: `--state`
```

次を Kiro Chat へ送ります。

```text
Checkpoint の復元演習です。docs/operations.md の `filter_option` の値だけを `--status` から `--state` へ変更してください。変更するのはその1行・その1ファイルだけです。Windows/macOS の command example、app.py、tests、data、他のファイルは変更せず、command と commit も実行しないでください。
```

変更後に確認します。

```powershell
git diff -- docs/operations.md
py -3.12 scripts/validate_docs.py
```

誤変更プロンプト直前の Checkpoint から Restore し、次を確認します。

```powershell
git status --short
py -3.12 scripts/validate_docs.py
```

Checkpoint は選んだ時点より後の Agent 変更と会話をまとめて戻します。Git commit とは別の安全網です。

# 7. Q&A・実務への転用

> **この章が役立つ場面:** 演習で学んだ方法を、自分の開発課題へ置き換えたいとき。
>
> **この章を終えると:** 自分の課題について Context、Steering、Hook、人の判断を1つずつ設計できるようになります。

次を自分の業務へ置き換えて記入します。

```text
現在の開発で困っていること:

最初に使う Context と理由:

場所が分かった後に絞る Context:

次回も守る Steering:

機械的に判定できる Hook / validator:

人の判断に残すこと:
```

振り返り:

1. 選択範囲だけの場合と、関連ファイルも追加した場合で何が変わったか
2. Context を減らすことで、何が判断しやすくなったか
3. 毎回繰り返している注意のうち、Steering または Hook に移せるものは何か
4. validator で機械的に判定することと、人がレビューすることをどう分けるか

最後にチャットタブを右クリックして **Export Chat** を選べます。ZIP には会話、コード、path、sub-execution が含まれる可能性があるため、外部共有前に必ず内容を確認します。

# 8. 最終確認

> **この章が役立つ場面:** 作業完了を感覚ではなく、tests、validator、CLI output で確認したいとき。
>
> **この章を終えると:** 意図した変更だけが入り、アプリケーションとドキュメントが整合していることを証明できます。

```powershell
py -3.12 -m unittest discover -s tests -v
py -3.12 scripts/validate_docs.py
py -3.12 app.py --status open
```

テストと validator が成功し、`JOB-001` と `JOB-003` が表示されれば完了です。
