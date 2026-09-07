# 運用手順

## ローカル検証

### Windows PowerShell

```powershell
py -3.12 -m unittest discover -s tests -v
py -3.12 scripts/validate_docs.py
```

### macOS / Linux

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_docs.py
```

## CLI contract

- `filter_option`: `--state`

## 絞り込み例

```powershell
py -3.12 app.py --state open
```

成功すると架空の求人を tab-separated text で表示します。network や production dependency はありません。
