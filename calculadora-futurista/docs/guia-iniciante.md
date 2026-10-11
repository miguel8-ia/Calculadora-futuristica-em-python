# Guia para iniciantes (VS Code)

1. **Instalar o Python:** python.org/downloads → baixe o instalador. No Windows, **marque "Add python.exe to PATH"** e clique em Install Now. Teste: abra o terminal e rode `python --version`.
2. **Instalar o VS Code:** code.visualstudio.com → instalar. Em Extensões (Ctrl+Shift+X), instale **Python** (Microsoft).
3. **Criar a pasta:** crie `calculadora-futurista` em Documentos.
4. **Abrir no VS Code:** File → Open Folder → escolha a pasta.
5. **Criar as pastas:** no painel Explorer, botão "New Folder": `src`, `tests`, `assets`, `docs`.
6. **Criar os arquivos** (botão "New File") nos caminhos exatos: `src/main.py`, `src/calculator.py`, `src/interface.py`, `src/keyboard.py`, `src/config.py`, `tests/test_calculator.py`, `assets/README.md`, `docs/architecture.md`, `docs/development.md`, `docs/commits.md`, `README.md`, `requirements.txt`, `pytest.ini`, `.gitignore`, `LICENSE`.
7. **Copiar o conteúdo** de cada arquivo (do .zip) e salvar com Ctrl+S. (Se usar o .zip, basta extrair e abrir a pasta.)
8. **Abrir o terminal:** menu Terminal → New Terminal.
9. **Criar o ambiente virtual:** `python -m venv .venv`
   Ativar: Windows `.venv\Scripts\Activate.ps1` | Linux/macOS `source .venv/bin/activate`. Aparece `(.venv)` no início da linha.
10. **Instalar dependências:** `pip install -r requirements.txt`
11. **Executar:** `python src/main.py`
12. **Testar:** `pytest`
13. **Inicializar o Git:** instale em git-scm.com, depois `git init` e `git branch -M main`.
14. **Criar o repositório no GitHub:** github.com → New repository → nome `SEU_REPOSITORIO` → sem README/licença → Create.
15. **Primeiro push:** faça os commits de `docs/commits.md` e depois
    `git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git` e `git push -u origin main`.
    O GitHub pedirá login no navegador na primeira vez.
