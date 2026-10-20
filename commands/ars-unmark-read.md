---
name: ars-unmark-read
description: 文献の既読申告を取り消す
disable-model-invocation: true
---

本人が指定した文献の既読申告を取り消す．
--passport-pathで対象ファイルを指定する．
記録は削除せず取消日時を残す．

```sh
python3 scripts/ars_mark_read.py $ARGUMENTS --unmark
```

scripts/はプラグインのルートから解決する．
