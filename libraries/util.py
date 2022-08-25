import re
import lxml.html

def is_base64(data: str) -> bool:
    data = plain_str(data)
    result = re.search("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$", data)
    if result:
        return True
    else:
        return False

def is_html(data: str) -> bool:
    html = re.compile('<.*?>')
    return bool(re.match(html, data))
    #return lxml.html.fromstring(data).find('.//*') is not None

def plain_str(data: str) -> str:
    return "".join([s for s in data.replace('\r\n','').replace('\n','').splitlines(True) if s.strip()])