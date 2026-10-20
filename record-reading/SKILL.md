---
name: record-reading
description: 文献の既読申告を管理する
---

# 文献の既読申告を管理する

本人が申告した文献と読んだ範囲を記録・取消する．
申告を実読・読解の証拠に置き換えない．
補助処理は[ars_mark_read.py](../scripts/ars_mark_read.py)を使う．
実行前に--helpで引数を確認する．
--passport-pathで本人が指定した対象を渡す．
記録では--scope，部分読みでは--locatorも指定する．
取消では--unmarkを使い，記録を消さず取消日時を残す．
対象と範囲が不明なら，変更前に本人へ確認する．
