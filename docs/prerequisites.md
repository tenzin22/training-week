# 事前準備 - Kiro IDE 1.x

確認日: 2026-09-03

## 必須環境

- Kiro IDE 1.x をインストールし、サインイン済みであること
- `starter-project` を Kiro IDE の `File > Open Folder` で開けること
- Kiro パネルの Steering、Agent Hooks、MCP Servers を表示できること
- Kiro IDE 内蔵 Terminal で Python 3.12 を実行できること
- draw.io Desktop または [draw.io Web](https://app.diagrams.net/) で `.drawio` を開いて保存できること
- 追加依存関係、顧客データ、認証情報を演習へ持ち込まないこと

本演習は Kiro IDE 専用です。CLI 専用の Tool Search や CLI の操作説明は使用しません。Terminal はスタータープロジェクトのテストと validator 実行にだけ使用します。

## Python 3.12 が見つからない場合

会社管理端末では、最初に自社のソフトウェア配布・承認ルールを確認してください。インストール権限がない場合は、管理者またはヘルプデスクへ Python 3.12 の導入を依頼します。

### macOS

推奨: [Python公式ダウンロード](https://www.python.org/downloads/macos/) から Python 3.12 の macOS 64-bit universal2 installer を入れます。

Homebrew の利用が許可され、すでに導入済みの場合は次でも構いません。

```bash
brew install python@3.12
python3.12 --version
```

インストール後に Kiro IDE を終了して再起動し、内蔵 Terminal で `python3 --version` または `python3.12 --version` を確認します。

### Windows

`winget` の利用が許可されている場合は PowerShell で実行します。

```powershell
winget install --exact --id Python.Python.3.12
py -3.12 --version
```

または [Python公式ダウンロード](https://www.python.org/downloads/windows/) から Python 3.12 の Windows installer (64-bit) を使用します。インストーラーでは **Add python.exe to PATH** を有効にしてください。

インストール後に Kiro IDE を終了して再起動し、内蔵 Terminal で `py -3.12 --version` を確認します。

## Git が見つからない場合

Checkpoint 自体は Git に依存しませんが、本演習の `#Git Diff`、Source Control、差分確認には Git repository と初期 commit が必要です。

Kiro IDE 内蔵 Terminal で確認します。

```bash
git --version
```

### Windows

`git` が見つからず、`winget` の利用が許可されている場合は PowerShell で実行します。

```powershell
winget install --exact --id Git.Git
```

または [Git for Windows](https://git-scm.com/download/win) からインストールします。導入後は Kiro IDE を終了して再起動し、内蔵 Terminal で `git --version` を再確認します。

### macOS

[Git 公式ダウンロード](https://git-scm.com/download/mac) を使用するか、Homebrew の利用が許可されている場合は次を実行します。

```bash
brew install git
git --version
```



## Kiro IDE 1.x の安全設定

1. `Settings > Agent > Agent Autonomy` を確認する。
2. 初回実施は `Supervised` を推奨する。
3. ファイル書き込み、コマンド、MCP ツールの承認画面では、まず 1 回限りの `Allow` を選ぶ。
4. `Always allow` を選ぶ場合は、対象ツールとこの workspace に範囲を限定する。
5. `.env`、鍵、資格情報、外部送信、自動コミットを許可しない。

Kiro IDE 1.x は capability-based permissions を使用します。未許可の書き込み、コマンド、MCP 呼び出しは承認を求めます。`deny > ask > allow` のため、組織またはユーザーの deny は workspace の allow で上書きできません。

## ハンズオンで使う Kiro IDE の操作確認（任意）

次の操作を確認します。利用できない場合も演習は継続できます。

- コードまたは文章を選択し、macOS の `Cmd+L`、Windows/Linux の `Ctrl+L` で現在のチャットへ追加できる
- 新規チャットへ追加する場合は `Cmd+Shift+L` または `Ctrl+Shift+L` を使える
- チャットタブを右クリックし、**Open in Editor** で Dockable Chat を開ける
- チャットタブを右クリックし、**Export Chat** を選択できる

選択範囲は Ask Kiro の現在または新しいチャットへ追加します。Export Chat の ZIP には会話、セッション情報、サブ実行が含まれるため、共有前に内容をレビューします。

## draw.io MCP の事前準備

本演習の Track A は、公式の stdio MCP Tool Server **`@drawio/mcp` v1.5.0** を使用します。これは図をブラウザー版 draw.io で開く方式です。MCP Apps 対応ホスト向けの `https://mcp.draw.io/mcp`（チャット内表示用 App Server）は使用しません。

会社管理端末では、Node.js と npm パッケージの利用が組織のソフトウェア・ネットワークポリシーで許可されていることを先に確認してください。

### 1. Node.js を確認する

`@drawio/mcp` は Node.js 18 以上が必要です。Kiro IDE 内蔵 Terminal で確認します。

```bash
node --version
npm --version
npx --version
```

Node.js 18 以上と npm / npx のバージョンが表示されれば、次へ進みます。

#### macOS で Node.js が見つからない場合

推奨: [Node.js 公式ダウンロード](https://nodejs.org/en/download) から LTS 版をインストールします。

Homebrew の利用が許可され、すでに導入済みの場合は次でも構いません。

```bash
brew install node@22
node --version
npm --version
```

#### Windows で Node.js が見つからない場合

`winget` の利用が許可されている場合は PowerShell で実行します。

```powershell
winget install --exact --id OpenJS.NodeJS.LTS
node --version
npm --version
```

または [Node.js 公式ダウンロード](https://nodejs.org/en/download) から Windows Installer の LTS 版を使用します。

#### Node.js をインストールした後（macOS / Windows 共通）

Node.js のインストールで更新された `PATH` を Kiro 本体と MCP process に読み込ませる必要があります。**Terminal を閉じる、ウィンドウを Reload するだけでは不十分です。**

1. 編集中のファイルを保存する
2. Kiro IDE の全ウィンドウを閉じ、**Kiro IDE を完全に終了する**（macOS は **Kiro > Quit Kiro**、Windows は **File > Exit**）
3. Kiro IDE を起動し直し、`starter-project` を再度開く
4. 新しい内蔵 Terminal で次を確認する

```bash
node --version
npm --version
npx --version
```

この完全終了・再起動が終わるまで MCP 設定へ進みません。Node.js 18 以上と npm / npx が確認できてから `@drawio/mcp` を設定します。

### 2. Kiro の MCP 設定を手動で追加する

Kiro Agent に「draw.io MCP を追加して」と依頼すると、Kiro の安全ポリシーにより `~/.kiro/settings/` または `.kiro/settings/` への書き込みが拒否される場合があります。これは異常ではありません。**Agent に権限を迂回させず、人が MCP 設定を手動編集します。**

本演習では他のプロジェクトへ影響しないよう、`starter-project` 内の workspace 設定を推奨します。

#### Windows（参加者向け推奨手順）

1. Kiro IDE で `starter-project` を開きます。
2. 内蔵 PowerShell Terminal が `starter-project` をカレントフォルダーとしていることを確認します。
3. 次を実行し、workspace 設定用フォルダーとファイルを開きます。

```powershell
New-Item -ItemType Directory -Force .kiro\settings
notepad .kiro\settings\mcp.json
```

4. ファイルが空の場合は、次をそのまま貼り付けて保存します。

```json
{
  "mcpServers": {
    "drawio": {
      "command": "npx",
      "args": ["--yes", "@drawio/mcp@1.5.0"],
      "disabled": false
    }
  }
}
```

5. すでに `mcpServers` 内に他の server がある場合は、既存設定を削除せず、直前の server の閉じ括弧 `}` の後にカンマを追加して `drawio` エントリだけを追記します。

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "example-command",
      "args": []
    },
    "drawio": {
      "command": "npx",
      "args": ["--yes", "@drawio/mcp@1.5.0"],
      "disabled": false
    }
  }
}
```

6. Notepad を閉じ、Kiro IDE へ戻ります。

Kiro の MCP Servers パネルから workspace MCP configuration を開ける場合は、PowerShell と Notepad の代わりにその画面で同じ JSON を手動保存しても構いません。

> Windows の注意: `%USERPROFILE%\.kiro\settings\mcp.json` はすべての workspace に適用されるユーザー設定です。本演習では `<starter-project>\.kiro\settings\mcp.json` を使い、影響範囲を限定します。

#### macOS

1. Kiro IDE で `starter-project` を開きます。
2. MCP Servers パネルから workspace MCP configuration を開くか、内蔵 Terminal で次を実行します。

```bash
mkdir -p .kiro/settings
open -e .kiro/settings/mcp.json
```

3. Windows と同じ JSON を手動で貼り付けて保存します。
4. 既存 server がある場合は、既存設定を残して `drawio` エントリだけを追加します。

### 3. 接続を確認する

1. MCP Servers パネルで `drawio` を Restart または Refresh します。反映されない場合は Kiro IDE を一度終了して再起動します。
2. 初回は `npx` が `@drawio/mcp@1.5.0` を取得するため、ネットワークによって少し時間がかかります。
3. 状態が `Connected` になることを確認します。
4. 次のツールが表示されることを確認します。

- `open_drawio_mermaid`
- `open_drawio_xml`
- `open_drawio_csv`
- `search_shapes`
- `list_pages` / `get_page` / `set_page`

5. 本演習では主に `open_drawio_mermaid` を使用します。
6. 初回の MCP 権限要求では、server 名が `drawio`、tool 名が `open_drawio_mermaid` であることを確認し、workspace に限定した 1 回限りの `Allow` を選びます。

`@drawio/mcp` は生成した図をブラウザー版 draw.io で開きます。**draw.io のブラウザー拡張機能は不要です。**

### 4. Track A / Track B を判定する

次をすべて満たす場合は Track A を使用します。

- Node.js 18 以上、npm、npx が利用できる
- MCP Servers パネルで `drawio` が `Connected`
- `open_drawio_mermaid` が表示される
- `https://app.diagrams.net/` をブラウザーで開ける

次のいずれかなら Track B を使用します。

- Node.js、npm、npx、npm registry、または外部ブラウザー利用が承認されていない
- draw.io MCP が未接続、または `open_drawio_mermaid` が表示されない
- 接続確認に 5 分以上かかる
- 権限プロンプトを安全に承認できない

Track B は Kiro に Mermaid または構造化図面仕様を作らせ、draw.io の `Arrange > Insert > Mermaid`、または手作業で再現します。

> データ取扱い: `@drawio/mcp` は図を URL の `#fragment` に格納してブラウザー版 draw.io を開くため、図データ自体は draw.io サーバーへ送信されません。ただし、draw.io の Web アプリ資産は外部から読み込まれます。また図の生成内容は利用中の LLM に渡るため、本演習では合成データだけを使用します。

## Agent Hooks の設定確認

本教材の Hook 設定は次の形式を使用します。

- 保存場所: `.kiro/hooks/*.json`
- schema: `"version": "v1"`
- 保存後トリガー: `PostFileSave`
- action: `command` または `agent`

オンデマンドの確認は `inclusion: manual` の Steering をチャットで選択して実施します。

## 公式資料

- [Steering](https://kiro.dev/docs/steering/)
- [Hooks v1](https://kiro.dev/docs/ide/whats-new-v1/hooks/)
- [MCP](https://kiro.dev/docs/mcp/)
- [Permissions](https://kiro.dev/docs/permissions/)
- [Checkpoints and rewind](https://kiro.dev/docs/checkpoints/)
- [Source Control](https://kiro.dev/docs/ide/editor/source-control/)
- [Powers の導入](https://kiro.dev/docs/powers/installation/)
- [draw.io MCP server](https://www.drawio.com/docs/manual/generate/drawio-mcp-server/)
- [draw.io Mermaid](https://www.drawio.com/docs/manual/mermaid/)
