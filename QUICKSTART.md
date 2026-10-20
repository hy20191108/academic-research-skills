# 導入

Claude Codeではこのforkを登録する．

```text
/plugin marketplace add hy20191108/academic-research-skills
/plugin install academic-research-skills@academic-research-skills
```

Codexでは必要なスキルのディレクトリを登録する．
補助ツールを使う時はリポジトリ全体を取得する．
Piではリポジトリのルートで`pi install .`を実行する．
ClaudeのフックはPiでは動かない．

ローカルの確認にはPython 3.11以上，uv，Node.jsが必要．

```sh
uv sync --locked
uv run --locked python scripts/check_repository.py
uv run --locked pytest -q
node --test tests/pi-skills.test.mjs
```

ネットワークを使う文献検索は利用環境の権限に従う．
