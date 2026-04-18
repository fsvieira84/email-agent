# Email Reader Agent 📧

Agente autônomo para leitura e processamento de e-mails.

## Funcionalidades
- Conectar a conta de e-mail via IMAP
- Ler e-mails não lidos
- Extrair informações principais
- Categorizar por prioridade
- Gerar resumos automáticos

## Instalação
```bash
pip install -r requirements.txt
```

## Uso
```python
from email_agent import EmailAgent

agent = EmailAgent("seu_email@gmail.com", "sua_senha")
emails = agent.fetch_unread_emails()
agent.process_emails(emails)
```

## Autor
GitHub Learn Project
