import re
from typing import List, Dict, Optional

class TransactionDetector:
    def __init__(self):
        self.financial_domains = [
            'sbi.co.in',
            'hdfcbank.com',
            'hdfcbank.net',
            'icicibank.com',
            'axisbank.com',
            'phonepe.com',
            'googlepay.com',
            'razorpay.com',
            'paypal.com'
        ]

        self.transaction_keywords = [
            'debited',
            'debit', 
            'withdrawn', 
            'charged'
        ]

        self.credit_keywords = [
            'credited',
            'received',
            'refunded',
            'refund',
            'credit',
            'deposit',
            'reward',
            'cashback'
        ]

    def is_transaction_email(self, sender: str, subject: str, snippet: str) -> bool:
        if self._is_financial_sender(sender):
            return True
        
        if self._contains_transaction_keywords(subject, snippet):
            return True
        return False
    
    def _is_financial_sender(self, sender: str) -> bool:
        return any(domain in sender.lower() for domain in self.financial_domains)
    
    def _contains_transaction_keywords(self, subject: str, snippet: str) -> bool:
        text = f"{subject} {snippet}".lower()
        return any(keyword in text for keyword in self.transaction_keywords)
    
    def extract_vendor(self, subject: str, snippet: str, sender: str) -> str:
        text = f"{subject} {snippet}"

        if '@' in sender:
            if '<' in sender:
                bank_name = sender.split('<')[0].strip()
                bank_name = re.sub(r'\s+(Alerts?Bank|Notifications?)$', '', bank_name, flags=re.IGNORECASE)
                if bank_name:
                    return bank_name
            
            domain = sender.split('@')[1].replace('>', '')
            if 'bank' in domain.lower():
                bank_name = domain.split('.')[0].title()
                return bank_name
        
        patterns = [
            r'at\s+([A-Z][A-Za-z\s&.-]+)',
            r'to\s+([A-Z][A-Za-z\s&.-]+)', 
            r'from\s+([A-Z][A-Za-z\s&.-]+)',
            r'for\s+([A-Z][A-Za-z\s&.-]+)',
            r'via\s+([A-Z][A-Za-z\s&.-]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        return sender.split('@')[0] if '@' in sender else sender 