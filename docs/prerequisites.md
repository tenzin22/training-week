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

本演習の推奨ルートは、Kiro IDE から公式の hosted MCP server **`https://mcp.draw.io/mcp`** へ接続する方法です。この構成は本演習の Windows 環境で動作確認済みです。Node.js や npm のインストールは不要です。

!!! note "本演習で使う構成"
    hosted MCP server を使います。ローカルの `@drawio/mcp` Tool Server は、発展的な代替構成として紹介するだけで、必須ではありません。

### 1. Kiro の MCP 設定を手動で追加する

Kiro Agent に MCP 設定の編集を依頼すると、安全ポリシーにより `.kiro/settings/` への書き込みが拒否される場合があります。Agent に権限を迂回させず、人が workspace 設定を手動編集します。

1. Kiro IDE で `starter-project` を開く
2. `starter-project/.kiro/settings/mcp.json` を開く。ファイルやフォルダーがなければ作成する
3. 次を貼り付けて保存する

```json
{
  "mcpServers": {
    "drawio": {
      "type": "http",
      "url": "https://mcp.draw.io/mcp",
      "disabled": false
    }
  }
}
```

既存の `mcpServers` がある場合は削除せず、`drawio` entry だけを追加します。

> `%USERPROFILE%\.kiro\settings\mcp.json` や `~/.kiro/settings/mcp.json` はすべての workspace に影響します。本演習では `starter-project/.kiro/settings/mcp.json` を使います。

### 2. 接続を確認する

1. MCP Servers パネルで `drawio` を Restart または Refresh する
2. 反映されない場合は Kiro IDE を完全に終了して起動し直す
3. 状態が `Connected` になることを確認する
4. `create_diagram` と `search_shapes` が表示されることを確認する
5. 初回の権限要求では server 名と tool 名を確認し、workspace に限定した1回限りの `Allow` を選ぶ

### 3. `connection closed` になる場合

まず JSON の `type` が `http`、URL が `https://mcp.draw.io/mcp` であることを確認します。古い stdio 設定のままの場合は、次のような entry が残っていないか確認します。

```json
"command": "npx"
```

Windows では MCP runner が `npx.cmd` を直接起動できず、`connection closed` になることがあります。本演習では hosted 構成へ切り替えます。

### 4. ローカル Tool Server を使いたい場合（本ハンズオンの対象外）

ローカルで Mermaid、CSV、XML の各 tool を使いたい場合は `@drawio/mcp@1.5.0` を stdio で起動できます。これは任意の発展構成です。

Windows:

```json
{
  "mcpServers": {
    "drawio": {
      "command": "cmd",
      "args": ["/c", "npx", "--yes", "@drawio/mcp@1.5.0"],
      "disabled": false
    }
  }
}
```

macOS / Linux:

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

ローカル構成では Node.js 18 以上が必要です。Node.js を新しくインストールした場合は Kiro IDE を完全に終了して起動し直します。接続後は `open_drawio_mermaid`、`open_drawio_xml`、`open_drawio_csv` などが表示されます。

### 5. 代替手段を選ぶ

- hosted server が `Connected` で `create_diagram` が使える: Track A
- hosted server が利用できない: Track B の Mermaid 手動 import
- ローカル Tool Server を試す: 演習後の発展項目

> データ取扱い: hosted MCP server では、図データが MCP request として draw.io server へ送信されます。本演習では合成データだけを使用し、顧客情報、個人情報、認証情報、社内構成を含めません。ローカル `@drawio/mcp` Tool Server は図を URL fragment に格納するため、図データ自体は draw.io server へ送信されません。

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
