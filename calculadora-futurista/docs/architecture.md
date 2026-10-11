# Arquitetura

## Princípio: LÓGICA ≠ INTERFACE

`calculator.py` não importa Tkinter e não sabe que existe uma tela.
`interface.py` não faz contas: apenas chama métodos de `Calculator`
e mostra o que ele devolve.

## Responsabilidades

| Arquivo | Responsabilidade |
|---------|------------------|
| `src/main.py` | Cria `Calculator` e `CalculatorUI` e inicia o programa |
| `src/calculator.py` | Estado e regras: entrada de dígitos, operadores, `=`, `%`, ±, apagar, limpar, erros. Usa `Decimal`, nunca `eval()` |
| `src/interface.py` | `CalculatorUI` (janela e eventos), `NeonButton` (botão 3D animado), `DisplayPanel` (display), `Backdrop` (fundo) |
| `src/keyboard.py` | Traduz teclas físicas em ações (`"digit:7"`, `"equals"`...) |
| `src/config.py` | Cores, fontes, tamanhos e layout dos botões |
| `tests/test_calculator.py` | Testes da lógica, sem abrir janela |

## Fluxo da aplicação

1. `main.py` cria a `Calculator` e a `CalculatorUI`.
2. A UI monta o layout com `grid` e `weight` (responsivo) a partir de `config.BUTTON_LAYOUT`.
3. Um clique (ou tecla) gera uma **ação** em texto, como `op:+`.
4. `CalculatorUI._dispatch` chama o método correspondente de `Calculator`.
5. A UI lê `display`, `expression` e `has_error` e redesenha o `DisplayPanel`.

## Efeito 3D

Cada botão é um `Canvas` com: halo neon (hover), corpo escuro (lateral), face,
brilho de vidro na metade superior e borda. Ao pressionar, a face desce
sobre o corpo; ao soltar, volta. A animação só roda enquanto há mudança
(~60 quadros/s), então o consumo em repouso é zero.
