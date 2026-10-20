# 中国語文献クライアントの試験用応答（#595）

scripts/test_chinese_literature_client.pyが，ここに保存した応答本文を実際のchinese_literature_client.pyへ渡す．URLの組立て，送信処理，本文解析，タイトルの確認，順次照会の結果集約は実装を動かし，通信部分だけを模擬する．他のtransport_bodies/<resolver>/と同じ方式である．

## 作成条件と限界

すべての応答本文は合成データである．4つの接続先が公開する形式に基づく．基にした手動確認の実例（2026-07-27に再確認）は，上流版のdeep-research/references/chinese_literature_api_protocol.mdに記録されている．実在するレコード，個人名，認証情報は含まない．
識別子には合成と分かる接尾辞を使う．実際のDOI名前空間について主張するものではない．他の試験データのREADMEには，初稿のもっともらしい識別子が実在論文を指した事例がある（モデル間レビューP1）．

- 10.5555はCrossrefに登録され，解決可能なDOIも存在する．10.5555/ars.cn.istic.*と10.5555/ars.cn.cnki.*は合成の振分け用であり，試験でDOIサービスへ接続せず，この接頭辞で実在DOIを発行できないとも仮定しない．
- ra_istic.jsonとra_cnki.jsonのRAは合成の応答である．10.5555の実際の登録先はISTICやCNKIではない．実際の対応（10.3760→ISTIC，10.13209→CNKI，10.1360→Crossref）は上流の資料に日付付きで記されている．ここでは3つの分岐だけを試す．
- ra_unknown_prefix.jsonは未知の接頭辞に対する実際の形式を使う．2026-07-27の確認では/doiRA/10.99999は[{"DOI": "10.99999", "status": "DOI does not exist"}]を返し，RAの代わりにstatusがある．10.99999はDOI Foundationが存在しないと報告する接頭辞である．
- PMIDの999999901と999999902はPubMedの割当範囲を大きく超える．ISSNの0000-0000は他の試験データと同じく，構造上無効な仮の値である．
- 雑誌「合成测试医学杂志」／Hecheng Ceshi Yi Xue Za Zhi，著者Hecheng Ceshi，すべての題名は架空である．雑誌はjournal_map=から渡すため，内蔵の初期対応表には依存しない．
- 論文ページのURLには予約済みの.invalidドメインを使う．

## ファイルと確認対象

| ファイル | 確認する応答形式 |
| --- | --- |
| ra_istic.json / ra_cnki.json / ra_crossref.json | doi.org/doiRA/<prefix>の3つの分岐 |
| ra_unknown_prefix.json | RAがなくstatusがある応答．サービス障害ではなく登録機関なしと判定する |
| istic_csl_hit.json | 中国語タイトルを持つCSL-JSON |
| istic_csl_other_title.json | 同じDOIが異なる題名を返す，引用情報の混成例 |
| cnki_landing_page.html | CSL-JSONの要求にCNKIが返すHTML．意図的に解析しない |
| handle_exists.json | Handle RESTのresponseCode: 1 |
| handle_absent.json | responseCode: 100．架空の識別子 |
| handle_internal_error.json | responseCode: 2．状態不明として機能低下を扱う |
| esearch_coverage_hit.json / esearch_coverage_zero.json | 雑誌のPubMed収録確認．1件以上と0件 |
| esearch_coordinate_hit.json / _zero.json / _ambiguous.json | [ta]+[vi]+[pg]による検索．一意の候補，架空のページ，複数候補 |
| esummary_hit.json | 中国語論文についてPubMedが保持する，角括弧付きの英語題名を含むesummaryの抽出結果 |
| esummary_no_doi.json | 巻・頁などが一致する一意の候補だがDOIがない．未検証のままとする |
| esummary_unknown_ra.json | 合成の未知接頭辞を持つDOI．登録機関なしと識別子の不一致を混同しない |
| esummary_year_mismatch.json | 巻・頁などは一致するが年が異なる |
| esummary_issn_mismatch.json | 雑誌のISSNが対応表のISSNと異なる |
| error_5xx.html | HTTPErrorに添付する5xxの本文．実装はコードと理由だけを読む |

実際のネットワークへ接続する試験は含まない．上流資料の実例は手動確認の記録であり，自動試験ではない．CIはdoi.org，hdl.handle.net，NCBIへ接続しない．
