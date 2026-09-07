# Synthetic Job List CLI

架空の求人情報を表示する、Python 3.12 標準ライブラリだけの小さな CLI です。

## 開始状態

### Windows PowerShell

```powershell
py -3.12 -m unittest discover -s tests -v
py -3.12 scripts/validate_docs.py
py -3.12 app.py
```

### macOS / Linux

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_docs.py
python3 app.py
```

テスト3件は成功し、ドキュメント validator は意図的に3件のずれを報告します。演習では `app.py` を現行仕様として扱い、`docs/` だけを必要な箇所に絞って修正します。

## 構成

- `app.py`: JSON 読み込み、status 検証、絞り込み、表示
- `data/jobs.json`: 架空の求人3件
- `tests/test_app.py`: 標準ライブラリ `unittest` のテスト
- `docs/`: 意図的に古い説明
- `scripts/validate_docs.py`: コードとドキュメントの整合性チェック

外部パッケージ、`PYTHONPATH`、Web サーバー、データベースは使用しません。
