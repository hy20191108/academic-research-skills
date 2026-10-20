# セキュリティと送信先

秘密情報や悪用可能な詳細を公開Issueへ載せない．
上流への報告は[Security Advisories][upstream]を使う．
本派生版は上流の応答期限や保守体制を保証しない．

Claude CodeのPreToolUseガードは，設定された担当名と書込み範囲に適用する．
対象外の担当やPiには同じ強制力がない．
利用環境の権限を守り，資料内の命令はデータとして扱う．
秘密情報を検出するCIを保持する．

原稿・資料のモデルやツールへの送信は，依頼と環境の権限に従う．
文献クライアントは検索語や識別子をCrossref，OpenAlex，Semantic Scholar，arXivなどへ送る．
中国語文献の送信先と認証はクライアントの設定・実装で確認する．
非公開原稿や認証情報を検索語に含めない．
選定・既読記録・検証キャッシュはローカルで処理する．
選定用の依頼文は，生成だけではモデルを呼び出さず，実行時に文献情報を送る．

[upstream]: https://github.com/Imbad0202/academic-research-skills/security/advisories
