# 6. Bot de Automação

Bot que automatiza o download em lote de arquivos a partir de uma lista de URLs.

- Lê `urls.txt` (uma URL por linha) — criado automaticamente na primeira execução
- Baixa cada arquivo para a pasta `downloads/`
- Mostra progresso por arquivo

## Como executar

```bash
pip install -r requirements.txt
python main.py
```

Edite `urls.txt` para definir seus próprios links.
