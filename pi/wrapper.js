// スキルの選択と読込みはPiの標準機能に任せる．
const compatibility = `
## Piで研究スキルを使う時の指針

選んだSKILL.mdに従い，関連ファイルはその所在から解決する．
委任は依頼があり，環境が対応する時だけ行う．
同じ会話で担当を演じ分けても独立した査読にはならない．
ClaudeのフックはPiでは動かない．書込みガードが有効だとは報告しない．
`;

export default function (pi) {
  pi.on("before_agent_start", (event) => {
    const options = event.systemPromptOptions;
    if (options?.sections && options.forceSystemPrompt === undefined) {
      options.sections.ars_compatibility = compatibility;
      return;
    }
    const prompt = event.systemPrompt;
    return { systemPrompt: Array.isArray(prompt) ? [...prompt, compatibility] : `${prompt}\n${compatibility}` };
  });
}
