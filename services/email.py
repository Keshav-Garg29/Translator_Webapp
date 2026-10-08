from abc import ABC, abstractmethod
from typing import List, Optional

class EmailProvider(ABC):
    @abstractmethod
    def send_email(self, to_email: str, subject: str, body: str, attachments: Optional[List[str]] = None) -> bool:
        """Sends an email to the specified address."""
        pass

class FakeEmailProvider(EmailProvider):
    def send_email(self, to_email: str, subject: str, body: str, attachments: Optional[List[str]] = None) -> bool:
        """Logs email content to the console instead of sending a real email."""
        print("\n" + "="*50)
        print(f" [FakeEmail] SENDING EMAIL")
        print(f" To: {to_email}")
        print(f" Subject: {subject}")
        print(f" Body: {body}")
        if attachments:
            print(f" Attachments: {', '.join(attachments)}")
        print("="*50 + "\n")
        return True
