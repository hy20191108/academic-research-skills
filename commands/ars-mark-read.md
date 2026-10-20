---
name: ars-mark-read
description: 文献の既読申告を記録する
disable-model-invocation: true
---

本人が申告した文献と読んだ範囲だけを記録する．
入力のpassportファイルを確認し，スクリプトへ渡す．
範囲は--scope，部分読みの箇所は--locatorで指定する．
申告を実読・読解の証拠に置き換えない．

```sh
python3 scripts/ars_mark_read.py $ARGUMENTS
```

scripts/はプラグインのルートから解決する．
