"""
Email Reader Agent - Agente autônomo para leitura de e-mails
"""
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from typing import List, Dict


class EmailAgent:
    """Agente autônomo para gerenciar e-mails"""
    
    def __init__(self, email_address: str, password: str, imap_server: str = "imap.gmail.com"):
        """
        Inicializa o agente de e-mail
        
        Args:
            email_address: Endereço de e-mail
            password: Senha da conta
            imap_server: Servidor IMAP (padrão: Gmail)
        """
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.mail = None
        self.emails_processed = 0
        
    def connect(self) -> bool:
        """Conecta ao servidor de e-mail"""
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_address, self.password)
            print(f"✓ Conectado em {self.email_address}")
            return True
        except Exception as e:
            print(f"✗ Erro ao conectar: {e}")
            return False
    
    def fetch_unread_emails(self, max_emails: int = 10) -> List[Dict]:
        """
        Busca e-mails não lidos
        
        Args:
            max_emails: Número máximo de e-mails a buscar
            
        Returns:
            Lista de e-mails com metadados
        """
        try:
            self.mail.select("INBOX")
            status, email_ids = self.mail.search(None, "UNSEEN")
            
            emails = []
            email_id_list = email_ids[0].split()[:max_emails]
            
            for email_id in email_id_list:
                status, msg_data = self.mail.fetch(email_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])
                
                email_info = {
                    "from": msg.get("From", "Desconhecido"),
                    "subject": self._decode_header(msg.get("Subject", "Sem assunto")),
                    "date": msg.get("Date", "N/A"),
                    "body": self._get_email_body(msg),
                    "priority": self._calculate_priority(msg.get("Subject", ""))
                }
                emails.append(email_info)
            
            print(f"📬 {len(emails)} e-mail(s) não lido(s) encontrado(s)")
            return emails
            
        except Exception as e:
            print(f"✗ Erro ao buscar e-mails: {e}")
            return []
    
    def process_emails(self, emails: List[Dict]) -> None:
        """Processa e exibe e-mails"""
        print("\n" + "="*60)
        print("PROCESSANDO E-MAILS".center(60))
        print("="*60)
        
        for i, email_msg in enumerate(emails, 1):
            print(f"\n[{i}] Prioridade: {'🔴 ALTA' if email_msg['priority'] == 'high' else '🟡 NORMAL'}")
            print(f"    De: {email_msg['from']}")
            print(f"    Assunto: {email_msg['subject']}")
            print(f"    Data: {email_msg['date']}")
            print(f"    Prévia: {email_msg['body'][:100]}...")
            self.emails_processed += 1
        
        print("\n" + "="*60)
        print(f"Total processado: {self.emails_processed} e-mail(s)")
        print("="*60)
    
    def _decode_header(self, header: str) -> str:
        """Decodifica cabeçalho de e-mail"""
        try:
            decoded = decode_header(header)
            if decoded[0][1]:
                return decoded[0][0].decode(decoded[0][1])
            return decoded[0][0]
        except:
            return header
    
    def _get_email_body(self, msg: email.message.Message) -> str:
        """Extrai o corpo do e-mail"""
        if msg.is_multipart():
            for part in msg.get_payload():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
        return msg.get_payload()
    
    def _calculate_priority(self, subject: str) -> str:
        """Calcula prioridade baseado no assunto"""
        urgent_keywords = ["urgente", "important", "urgent", "!!", "ASAP"]
        return "high" if any(kw.lower() in subject.lower() for kw in urgent_keywords) else "normal"
    
    def filter_by_sender(self, emails: List[Dict], sender: str) -> List[Dict]:
        """Filtra e-mails por remetente"""
        return [e for e in emails if sender.lower() in e["from"].lower()]

    def disconnect(self) -> None:
        """Desconecta do servidor"""
        if self.mail:
            self.mail.close()
            self.mail.logout()
            print("✓ Desconectado")


# Script de demonstração
if __name__ == "__main__":
    # NOTA: Use variáveis de ambiente para armazenar credenciais
    # from dotenv import load_dotenv
    # import os
    # load_dotenv()
    # email_addr = os.getenv("EMAIL_ADDRESS")
    # password = os.getenv("EMAIL_PASSWORD")
    
    print("Email Reader Agent - Demo")
    print("Para usar: defina suas credenciais de e-mail")
