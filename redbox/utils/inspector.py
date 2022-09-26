from typing import Dict, List
from email.message import EmailMessage
from redbox.models.attachment import Attachment

class Inspector:

    def __init__(self, msg:EmailMessage):
        self.message = msg

    def get_headers(self) -> Dict[str, str]:
        return dict(self.message.items())

    def get_html_body(self) -> str:
        for pl in self.message.get_payload():
            content_type = pl['Content-Type'].split(";")
            if "text/html" in content_type:
                return pl.get_payload()
            elif "multipart/related" in content_type:
                return Inspector(pl).get_html_body()
            elif "multipart/alternative" in content_type:
                return Inspector(pl).get_html_body()

    def get_text_body(self) -> str:
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
