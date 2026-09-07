# アーキテクチャ

## 構成

1. User は任意の filter を付けて `app.py` を実行します。
2. `app.py` は架空の求人データを読み込みます。
3. 条件に一致する求人を tab-separated text で表示します。

## 保存形式

- `storage_format`: `csv`

starter implementation は CSV file から求人データを読み込みます。local storage のため network access は不要です。

## 境界

- authentication と authorization は実装しません。
- production system へ接続しません。
- 求人情報はすべて架空の演習データです。
