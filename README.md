# Calculadora Futurista 3D

## Sobre o projeto

Calculadora desktop em Python com visual de painel holográfico: fundo escuro,
botões com profundidade 3D, brilho neon, display digital e animações leves.
A lógica matemática é totalmente separada da interface e coberta por testes.


##**Demonstração da calculadora**




## Tecnologias

- Python 3.9+
- Tkinter (já incluído no Python — nenhuma dependência externa para rodar)
- Pytest (apenas para os testes)
- Git e GitHub

## Funcionalidades

- Adição, subtração, multiplicação e divisão
- Porcentagem, números decimais e números negativos (±)
- Limpar (C) e apagar último caractere (⌫)
- Operações encadeadas (2 + 3 × 4 = 20, da esquerda para a direita)
- Precisão decimal exata (0.1 + 0.2 = 0.3)
- Tratamento de divisão por zero e de resultados muito grandes
- Suporte completo ao teclado
- Janela redimensionável

## Interface

Camadas e sombras criam profundidade: o painel tem sombra deslocada, cada botão
tem uma lateral escura que "afunda" ao clicar, o hover acende a borda neon e o
display tem scanlines e brilho no texto. Paleta: `#05070D`, `#0B1020`,
`#111A2E`, destaque ciano `#00E5FF` e roxo `#7C3AED`.

## Estrutura do projeto

```
calculadora-futurista/
├── src/
│   ├── main.py          # ponto de entrada
│   ├── calculator.py    # lógica matemática (sem interface)
│   ├── interface.py     # janela, display, botões 3D, animações
│   ├── keyboard.py      # atalhos do teclado
│   └── config.py        # cores, fontes, layout dos botões
├── tests/
│   └── test_calculator.py
├── assets/README.md
├── docs/
│   ├── architecture.md
│   ├── development.md
│   ├── commits.md
│   └── guia-iniciante.md
├── pytest.ini
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Instalação

### Windows (PowerShell)

```powershell
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/main.py
```

Se o PowerShell bloquear a ativação, rode uma vez:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### Linux / macOS

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/main.py
```

No Linux (Debian/Ubuntu), se faltar o Tkinter: `sudo apt install python3-tk`.

## Executando os testes

```
pytest
```

## Como utilizar

Clique nos botões ou use o teclado. Digite um número, escolha a operação,
digite o segundo número e pressione `=`. A operação em andamento aparece em
cima, o número atual embaixo.

## Atalhos

| Tecla | Ação |
|-------|------|
| `0`–`9` | Números |
| `+` `-` | Soma / subtração |
| `*` ou `x` | Multiplicação |
| `/` | Divisão |
| `.` ou `,` | Ponto decimal |
| `%` | Porcentagem |
| `Enter` ou `=` | Resultado |
| `Backspace` | Apagar último caractere |
| `Esc` ou `Delete` | Limpar |

## Melhorias futuras

- Histórico de cálculos e exportação (CSV/TXT)
- Modo científico
- Temas (ciano, roxo, verde matrix)
- Sons de clique
- Animações mais avançadas
- Versão web
- Versão mobile

## Licença

MIT — veja o arquivo [LICENSE](LICENSE).
