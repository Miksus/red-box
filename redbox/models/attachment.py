from typing import Optional
from email.message import EmailMessage
from pydantic import BaseModel

class Attachment(BaseModel):
    filename: Optional[str]
    content: str
    content_type: str

    @staticmethod
    def _parse_disposition(payload:EmailMessage) -> dict:
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
    def from_message(cls, payload:EmailMessage):
        disposition = cls._parse_disposition(payload)

        return cls(
            content_type=payload['Content-Type'],
            content=payload.get_payload(),
            filename=disposition.get("filename").strip('"'),
        )
