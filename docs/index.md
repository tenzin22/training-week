# Kiro IDE 中級編: 開発中のコードに合わせたドキュメント整備

コード変更が先行して古くなったドキュメントを、Kiro IDE の Context、Steering、Agent Hooks、draw.io MCP、Checkpoints を使って安全に整備するハンズオンです。

<div class="hero-actions" markdown>
[参加者ガイドを開く](participant-guide.md){ .md-button .md-button--primary }
[Starter Project をダウンロード](assets/downloads/starter-project.zip){ .md-button }
</div>

## 学習できること

<div class="grid cards" markdown>

-   **必要な Context を選ぶ**

    選択範囲、`#File`、`#Folder`、Problems、`#Terminal`、`#Git Diff` を問いに応じて使い分けます。

-   **ルールを再利用する**

    Steering を `always`、`fileMatch`、`manual` に分けて設計します。

-   **検証を自動化する**

    Agent Hook から validator を実行し、ドキュメントのずれを検出します。

-   **安全に可視化・復旧する**

    draw.io の編集可能な図を作り、Checkpoint から誤変更を戻します。

</div>

## 当日の進め方

1. [事前準備](prerequisites.md)を確認する
2. Starter Project をダウンロードして Kiro IDE で開く
3. [参加者ガイド](participant-guide.md)に沿って進める
4. draw.io の章では [draw.io 統合ラボ](drawio-lab.md)を開く

!!! info "演習データ"
    すべて架空の求人データです。実在の人物、顧客、認証情報は使用しません。
