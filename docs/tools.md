# 補助ツールと送信先

| 仕事 | 実行するファイル |
| --- | --- |
| 文献を検索する | scripts/の各*_client.py |
| 既読申告を記録・取消する | scripts/ars_mark_read.py（取消は--unmark） |
| 指定文献の検証キャッシュを削除する | scripts/ars_cache_invalidate.py |

既読申告は読解の証拠ではなく，取消時も元の記録を残す．キャッシュ削除だけでは再検証にならない．
文献選定はskills/sr-screener/scripts/を使う．
prepare_records.pyで入力，build_workflow.pyで依頼生成，merge_decisions.pyで判断集約を行う．
本文確認はprepare_fulltext.py，結果出力はbuild_outputs.pyを使う．設定例は同スキルのtemplates/にある．
複数担当の生成は依頼がある時だけ行い，モデル名は利用環境に合わせる．引数は各ファイルの--helpを参照する．

検索語・文献識別子はCrossref，OpenAlex，Semantic Scholar，arXivなどへ送る．検索と主張の検証は区別する．
APIの利用条件と認証は実行前に確認する．中国語文献の送信先はクライアントの設定・実装に従う．
原稿・資料の送信は依頼と環境の権限に従い，非公開原稿や認証情報を検索語に含めない．
選定・既読記録・キャッシュはローカルで処理する．選定用の依頼文は生成だけではモデルを呼ばず，実行時に文献情報を送る．
Claude CodeのPreToolUseガードは設定された担当名と書込み範囲に適用する．対象外の担当やPiには同じ強制力がない．
秘密情報や悪用可能な詳細を公開Issueへ載せない．上流への報告は[Security Advisories][security]を使う．本派生版は上流の応答期限や保守体制を保証しない．

[security]: https://github.com/Imbad0202/academic-research-skills/security/advisories
