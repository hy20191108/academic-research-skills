# 第三者のプロジェクト

以下は上流版の第三者情報の日本語訳である．ARSを基にした実装，連携サービスと，ARSが仕組みを取り入れたプロジェクトを記載する．

## 掲載と利用について

掲載は推奨を意味しない．掲載内容はコミュニティから寄せられたもので，ARSの保守者はレビュー・試験・検証を行っていない．各運営者は本プロジェクトから独立している．
品質，安全性，プライバシー保護，継続提供を保守者が保証するものではない．外部サービスには独自の規約，料金，追跡，データ取扱方針がある．登録やアップロードの前に確認すること．
利用は自己責任とし，未公開研究，個人情報，機密資料を渡す前に方針を確認すること．本リポジトリの送信先とローカル保存先は[データの送信先](docs/DATA_FLOWS.md)を参照する．この説明は以下の第三者サービスには適用されない．

## 掲載申請と公式認定

上流版への掲載はIssueまたはプルリクエストで表への追加を申請する．ARSの名称と元リポジトリへのリンクを明示し，ARSと連携内容を正確に説明することが条件となる．条件違反，迷惑行為，マルウェアなどの有害な内容は，保守者が掲載を断るか削除できる．
掲載と公式の支援・同梱は異なる．移植や正式な連携を主要READMEで紹介し，同梱する場合は，より厳しいコミュニティ保守の移植方針（Platform Port Reminder）に従い，上流版のIssueで相談する．

## 掲載プロジェクト

説明は申請者の主張を中立的に記したもので，保守者による検証はない．

| プロジェクト | 運営者 | 内容 | リンク |
| --- | --- | --- | --- |
| ClawMama | kinhunt（第三者） | TelegramまたはWhatsAppでAcademic Research Pipelineの初回試用を提供する，OpenClaw/Hermes型のホスト型エージェント | [試用](https://app.clawmama.run/skills/639wu5/hermes?utm_source=github&utm_medium=issue&utm_campaign=skill_outreach_academic_research_skills) |
| OrcaRouter | OrcaRouterチーム | OpenAI・Anthropic互換ゲートウェイ．`ARS_OPENAI_COMPAT_BASE_URL`と`ARS_CROSS_MODEL`でモデル間検証に使う．`anthropic/claude-sonnet-5`などの名前空間付きモデルIDは，根拠資料に基づかないOpenAI互換経路で処理する | [orcarouter.ai](https://www.orcarouter.ai) |
| Academic Research Skills OpenClaw Port | ChunkyPanda29（第三者） | 4つのARSスキルをOpenClawへ移植し，各SKILL.mdの環境依存の表現を調整．書込み範囲のガードはフックではなく，スキルの手順として実行する | [リポジトリ](https://github.com/ChunkyPanda29/academic-research-skills-openclaw) |
| md-to-word | ls-open（第三者） | MarkdownからWord（.docx）へ決定的に組版する．プレーンテキストのrequirements.txtで配置を指定し，出力前後に自動確認する．中国語の学位論文・投稿用DOCXを対象とし，指示語は中国語で説明されている | [リポジトリ](https://github.com/ls-open/md-to-word) |

## ARSが参照したプロジェクト

ARSが仕組みを取り入れた独立プロジェクトへの謝辞であり，推奨や提携を意味しない．帰属は対応するIssueとプルリクエストにも記録されている．

| プロジェクト | 保守者 | 関係 | リンク |
| --- | --- | --- | --- |
| sci-ssci-skills | [@MissOrangePeel](https://github.com/MissOrangePeel)（Yila-AI） | v3.19.0の改稿時の主張変化を確認するガードが参照した，主張の強さの段階と決定的な不変条件確認の仕組み（#569，#570，[PR #571](https://github.com/Imbad0202/academic-research-skills/pull/571)） | [リポジトリ](https://github.com/Yila-AI/sci-ssci-skills) |
