# Git, GitHub e Commits

## Criar o repositório no GitHub

1. Entre em github.com → **New repository**.
2. Nome: `SEU_REPOSITORIO`. Deixe **sem** README, .gitignore e licença (o projeto já tem).
3. Clique em **Create repository**.

## Comandos básicos

```
git init
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
# ... faça os commits da sequência abaixo ...
git push -u origin main
```

Na primeira vez, configure seu nome: `git config --global user.name "SEU_NOME"`
e `git config --global user.email "seu@email.com"`.

## Sequência de commits (Conventional Commits)

Cada commit deixa o projeto em um estado que funciona.

### 1. `chore: inicializa estrutura do projeto`
```
git add .gitignore LICENSE requirements.txt assets/README.md
git commit -m "chore: inicializa estrutura do projeto"
```
- **Fez:** ignorou arquivos temporários, adicionou licença MIT, dependências e pasta de assets.
- **Por quê:** base limpa para o repositório.
- **Descrição:** "Neste commit foi criada a estrutura inicial do projeto, com licença, lista de dependências e regras para não versionar arquivos temporários. Essa organização facilita a manutenção e permite que novas funcionalidades sejam adicionadas futuramente."

### 2. `feat: implementa lógica da calculadora`
```
git add src/calculator.py
git commit -m "feat: implementa lógica da calculadora"
```
- **Fez:** classe `Calculator` com as quatro operações, %, ±, apagar, limpar e tratamento de erros.
- **Por quê:** a lógica é o núcleo e deve existir independente da interface.
- **Descrição:** "Neste commit foi implementada a lógica matemática usando Decimal, sem eval(), com tratamento de divisão por zero, resultados muito grandes e entradas inválidas. A calculadora não depende da interface, o que facilita testes e reutilização."

### 3. `test: adiciona testes da calculadora`
```
git add tests/test_calculator.py pytest.ini
git commit -m "test: adiciona testes da calculadora"
```
- **Fez:** testes de soma, subtração, multiplicação, divisão, divisão por zero, porcentagem, negativos, decimais, limpeza e operações encadeadas.
- **Por quê:** garantir que a lógica funciona e continue funcionando.
- **Descrição:** "Neste commit foram adicionados testes automatizados com pytest cobrindo operações, casos de erro e casos de borda. Eles rodam sem abrir janela e protegem a lógica contra regressões."

### 4. `feat: adiciona suporte ao teclado`
```
git add src/keyboard.py
git commit -m "feat: adiciona suporte ao teclado"
```
- **Fez:** mapa de teclas (0–9, + − * /, Enter, Backspace, Esc, ponto) e função `bind_keyboard`.
- **Por quê:** usabilidade; fica isolado da aparência.
- **Descrição:** "Neste commit foi criado o módulo que traduz teclas físicas em ações da calculadora, permitindo uso completo sem o mouse."

### 5. `feat: adiciona interface gráfica futurista`
```
git add src/config.py src/interface.py src/main.py
git commit -m "feat: adiciona interface gráfica futurista"
```
- **Fez:** janela responsiva, display digital, botões 3D com hover e efeito de pressionar, fundo em perspectiva.
- **Por quê:** entregar a experiência visual do projeto e conectar tudo.
- **Descrição:** "Neste commit foi criada a interface em Tkinter com visual holográfico, botões com profundidade e animações leves. A interface apenas chama a classe Calculator, mantendo lógica e aparência separadas."

### 6. `docs: adiciona documentação do projeto`
```
git add README.md docs/
git commit -m "docs: adiciona documentação do projeto"
```
- **Fez:** README, arquitetura, desenvolvimento e este guia.
- **Por quê:** quem abrir o repositório precisa entender e rodar o projeto.
- **Descrição:** "Neste commit foi adicionada a documentação com instalação, atalhos, estrutura e arquitetura, para que qualquer pessoa consiga executar e contribuir."

### 7. `style: aprimora interface e efeitos visuais`
Use este commit **depois** de personalizar algo, por exemplo mudar `ACCENT` em `src/config.py`:
```
git add src/config.py
git commit -m "style: aprimora interface e efeitos visuais"
```
- **Descrição:** "Neste commit foram ajustadas cores e efeitos visuais para melhorar contraste e identidade, sem alterar o comportamento."

> Os commits "chore: adiciona arquivos de configuração" foram absorvidos nos commits 1 e 3, porque `requirements.txt` e `pytest.ini` já são necessários nesses pontos.

Depois: `git push -u origin main`.
