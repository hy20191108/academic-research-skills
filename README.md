# Academic Research Skills

研究の仕事ごとに，短い指針を持つスキル集．

| スキル | 仕事 |
| --- | --- |
| [deep-research](deep-research/SKILL.md) | 研究の問いと文献を調べる |
| [academic-paper](academic-paper/SKILL.md) | 論文を執筆し推敲する |
| [academic-paper-reviewer](academic-paper-reviewer/SKILL.md) | 論文の主張と根拠を読む |
| [academic-pipeline](academic-pipeline/SKILL.md) | 研究から論文まで進める |
| [sr-screener](sr-screener/SKILL.md) | レビュー対象の文献を選ぶ |

## 利用

Claude Codeでは，このforkをプラグインとして登録する．

```text
/plugin marketplace add hy20191108/academic-research-skills
/plugin install academic-research-skills@academic-research-skills
```

スキルを直接呼ぶか，`/ars-plan`，`/ars-reviewer`，`/ars-full`などを使う．
他の環境では必要なスキルのディレクトリを登録する．

## このforkの変更

5つのSKILL.mdを，研究の問い・根拠・執筆に関する短い指針へ置き換えた．
本文で固定人数のエージェントや固定段階の進行を要求しない．
コマンドは対応するスキルへ依頼を渡す．
スキル名，補助ツール，参考資料，既存のガードは保持する．
補助資料は必要時に参照する．旧版固有の成果物形式は保証しない．

上流のエージェント，フック，Piアダプター，設計資料とテストは残している．
補助エージェントには旧版の役割別手順が残るが，標準では起動しない．
短い指針だけを使う場合は5つのスキルを個別に登録する．
上流の契約テストは短縮版の品質保証を表さない．

## 原著とライセンス

原著：[Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)．
Copyright © 2026 Cheng-I Wu．[CC BY-NC 4.0](LICENSE)．
hy20191108のforkでスキル本文，コマンド，選択規則と案内を変更した．
上流の著作権表示とライセンスは保持する．
