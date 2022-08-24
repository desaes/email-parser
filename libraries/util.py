import re
import html2text
import base64
import lxml.html
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.start_tags = list()
        self.end_tags = list()
        self.attributes = list()
    
    def is_text_html(self):
        return len(self.start_tags) == len(self.end_tags)

    def handle_starttag(self, tag, attrs):
        self.start_tags.append(tag)
        self.attributes.append(attrs)

    def handle_endtag(self, tag):
        self.end_tags.append(tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)




def is_base64(data: str) -> bool:
    data = plain_str(data)
    result = re.search("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$", data)
    if result:
        return True
    else:
        return False

def is_html(data: str) -> bool:
    return lxml.html.fromstring(data).find('.//*') is not None

def plain_str(data: str) -> str:
    return "".join([s for s in data.replace('\r\n','').replace('\n','').splitlines(True) if s.strip()])

def decode_str(data: str) -> str:
    if data:
        if is_base64(data):
            try:
                data = base64.b64decode(plain_str(data)).decode().replace('\t', '').strip()
            except Exception as e:
                pass

        if is_html(data):
            data = html2text.html2text(data)

        return data
    else:
        return None