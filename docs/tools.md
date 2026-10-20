# 補助ツール

文献クライアントはscripts/の各*_client.pyにある．
検索結果の取得と研究の主張の検証は別に行う．
各APIの利用条件と認証は実行前に確認する．

文献選定はsr-screener/scripts/を使う．
prepare_records.pyで入力を整理する．
build_workflow.pyで担当への依頼を生成する．
merge_decisions.pyで判断を集める．
prepare_fulltext.pyで本文確認の対象を準備する．
build_outputs.pyで選定結果を出力する．
引数は各スクリプトの--helpで確認する．
設定例はsr-screener/templates/にある．
元の複数担当方式を使う時だけ明示的に実行する．
例の担当モデル名は実際に利用できるものに置き換える．

既読記録はars_mark_read.py，取消は--unmarkを使う．
申告は読解の証拠ではなく，元の記録を残して取り消す．
ars_cache_invalidate.pyは指定文献のキャッシュを削除する．
これらは旧形式の入力を受け付ける互換ツールである．
