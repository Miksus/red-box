import datetime
import email
from email.message import EmailMessage as EmailMessageStd
from typing import List, Optional
from pydantic import BaseModel, Field, validator

class Inspector:

    def __init__(self, msg:EmailMessageStd):
        self.message = msg

    def get_headers(self) -> dict:
        return dict(self.message.items())

    def get_html_body(self)->str:
        for pl in self.message.get_payload():
            content_type = pl['Content-Type'].split(";")
            if "text/html" in content_type:
                return pl.get_payload()
            elif "multipart/related" in content_type:
                return Inspector(pl).get_html_body()
            elif "multipart/alternative" in content_type:
                return Inspector(pl).get_html_body()

    def get_text_body(self)->str:
        for pl in self.message.get_payload():
            content_type = pl['Content-Type'].split(";")
            if "text/plain" in content_type:
                return pl.get_payload()
            elif "multipart/related" in content_type:
                body = Inspector(pl).get_text_body()
                if body is not None:
                    return body
            elif "multipart/alternative" in content_type:
                body = Inspector(pl).get_text_body()
                if body is not None:
                    return body

    def get_attachments(self) -> List:
        # Mime types:
        #   text/plain: For textual files
        #   application/octet-stream: For all others
        for pl in self.message.get_payload():
            content_type = pl['Content-Type'].split(";")[0]
            if content_type.startswith("application/"):
                yield Attachment.from_message(pl)

class Attachment(BaseModel):
    filename: Optional[str]
    content: str
    content_type: str

    @staticmethod
    def _parse_disposition(payload:EmailMessageStd) -> dict:
        disp_str = payload['Content-Disposition']
        disps = {}
        for disp_line in disp_str.split(";"):
            disp_line = disp_line.strip()
            if len(disp_line.split("=")) > 1:
                key, val = disp_line.split("=", 1)
                disps[key] = val
            else:
                disps[disp_line] = None
        return disps
        
    @classmethod
    def from_message(cls, payload:EmailMessageStd):
        disposition = cls._parse_disposition(payload)

        return cls(
            content_type=payload['Content-Type'],
            content=payload.get_payload(),
            filename=disposition.get("filename").strip('"'),
        )

class EmailMessage(BaseModel):
    """Simplified representation of an email"""
    content: str = Field(description="Full email as string")

    received: str
    message_id: str
    
    message_date: datetime.datetime = Field(alias="date")
        
    from_: str
    subject: str
    to: List[str]
    cc: str = None
    bcc: str = None

    # Non-headers
    html_body: str
    text_body: str
    attachments: List[Attachment]

    @validator("to", pre=True)
    def parse_to(cls, value):
        return value.split(", ")

    @validator("message_date", pre=True)
    def parse_date(cls, value, values):
        return datetime.datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %z")
        
    @classmethod
    def from_string(cls, content:str):
        def format_field(f):
            f = f.lower().replace("-", "_")
            if f == "from":
                return "from_"
            return f

        msg = email.message_from_string(content)
        insp = Inspector(msg)
        headers = insp.get_headers()#dict(msg.items())

        html_body = insp.get_html_body()
        text_body = insp.get_text_body()
        attachments = insp.get_attachments()

        headers = {
            format_field(key): val
            for key, val in headers.items()
        }

        return cls(
            content=content,
            html_body=html_body,
            text_body=text_body,
            attachments=list(attachments),
            **headers
        )

    def __str__(self):
        return self.content

    def to_email(self):
        return email.message_from_string(self.content)