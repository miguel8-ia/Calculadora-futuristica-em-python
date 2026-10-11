# Desenvolvimento

## Ambiente

```
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
source .venv/bin/activate         # Linux/macOS
pip install -r requirements.txt
```

## Executar

```
python src/main.py
```

## Testar

```
pytest
```

## Como contribuir

1. Faça um fork e crie uma branch: `git checkout -b feat/minha-ideia`
2. Altere o código seguindo PEP 8 e adicione testes para mudanças na lógica.
3. Rode `pytest` e confirme que tudo passa.
4. Faça commits no padrão Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `style:`, `chore:`).
5. Abra um Pull Request descrevendo a mudança.
