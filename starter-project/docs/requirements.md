# 要件

## 目的

架空の求人一覧 CLI は、この演習用の求人情報を表示します。

## 対応データ

- `status`: `open`, `paused`
- 各求人は job ID、title、location、status を持ちます。

## 制約

- 例はすべて架空とします。
- 未対応の status は validation error にします。
- CLI は status で求人を絞り込めます。
