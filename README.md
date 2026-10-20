# 研究スキル

| 依頼 | スキル |
| --- | --- |
| 問いと文献を調べる | [deep-research](skills/deep-research/SKILL.md) |
| 論文を執筆・改稿する | [academic-paper](skills/academic-paper/SKILL.md) |
| 原稿を査読する | [academic-paper-reviewer](skills/academic-paper-reviewer/SKILL.md) |
| 研究から論文まで進める | [academic-pipeline](skills/academic-pipeline/SKILL.md) |
| 文献群から対象を選ぶ | [sr-screener](skills/sr-screener/SKILL.md) |

Claude Codeへの導入：
```text
/plugin marketplace add hy20191108/academic-research-skills
/plugin install academic-research-skills@academic-research-skills
```
Codexではskills/配下の必要なスキルを登録する．
Piではリポジトリのルートで`pi install .`を実行する．
[補助ツール](docs/tools.md)を使う時はリポジトリ全体を取得する．
導入後，仕事を自然文で依頼する．

原著はCheng-I Wuの[Academic Research Skills](https://github.com/Imbad0202/academic-research-skills)．
本派生版は指示・構成・補助処理を変更した．
[CC BY-NC 4.0](LICENSE)と[帰属表示](docs/attribution.md)を参照する．
