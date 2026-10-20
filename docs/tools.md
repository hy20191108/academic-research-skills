# 補助ツール

| 仕事 | 実行するファイル |
| --- | --- |
| 文献を検索する | scripts/の各*_client.py |
| 既読申告を記録・取消する | scripts/ars_mark_read.py（取消は--unmark） |
| 指定文献の検証キャッシュを削除する | scripts/ars_cache_invalidate.py |

既読申告は読解の証拠ではない．取消時も元の記録を残す．
キャッシュ削除だけでは再検証にならない．

文献選定はskills/sr-screener/scripts/を使う．
prepare_records.py → build_workflow.py → merge_decisions.pyで入力，依頼生成，判断集約を行う．
本文確認はprepare_fulltext.py，結果出力はbuild_outputs.pyを使う．
設定例は同スキルのtemplates/にある．
複数担当の生成は依頼がある時だけ行い，モデル名は利用環境に合わせる．
引数は各ファイルの--help，APIの利用条件と認証は実行前に確認する．
検索結果の取得と主張の検証は区別する．
