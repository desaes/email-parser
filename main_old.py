import os, sys
import imaplib
import email
from pprint import pprint


configs = [{
    "email": {
        "imap_host": "172.18.0.142",
        "imap_port": 143,
        "imap_user": "test",
        "imap_pass": "test",
        "mbox": "Inbox"
    },
    "filters": {
        "from": "ubuntu",
        "subject": "",
        "body": ""
    },
    "capture_text": {
        "from": {
            "field_00": "",
            "field_01" :""
            },     
        "subject": {
            "field_00": ""
            },
        "body": {
            "field_00": "",
            "field_01": ""
            },
    },
    "action": [{
        "api": {
            "target": "aranda",
            "endpoint_url": "http://api"
        }   
    }]
}
]

def filter(filters):
    """
    Build a text filter based on configuration filter
    """
    filter = ""
    for key, value in filters.items():
        if value:
            filter += f"{key.upper()} \"{value}\" "
    if filter:
        return f"({filter.rstrip()})"
    else:
        return "(ALL)"

def unpack_email(msgs):
    """
    Create a list with the message or messages (multipart)
    """
    result = []
    if msgs.is_multipart():
        result.append(msgs)
        for msg in msgs.get_payload():
            #if isinstance(msg, (list, tuple)):
            if hasattr(msg, "__iter__") and not isinstance(msg, str):
                result.extend(unpack_email(msg))
            else:
                result.append(msg)
    else:
        result.append(msgs)
    return result

for config in configs:
    filter = filter(config['filters'])
    try:
        imap = imaplib.IMAP4(config["email"]["imap_host"])
        imap.login(config["email"]["imap_user"], config["email"]["imap_pass"])
        imap.select(config["email"]["mbox"])
        (_, data) = imap.search(None, filter)
        for num in data[0].split():
            (_, data) = imap.fetch(num, '(RFC822)')
            msgs = email.message_from_string(data[0][1].decode('utf-8'))
            #print(f"{num}")
            for msg in unpack_email(msgs):
                if "To" in msg.keys():
                    for item in config["capture_text"].keys():
                        if item == "body":
                            #print(msg.get_payload())
                            for k,v in config["capture_text"][item].items():
                                print(k)
                        else:
                            print(msg[item])

    except Exception as e:
        print(f"Error: {e.message}")
        sys.exit()
    finally:
        try:
            imap.close()
        except Exception as e:
            print(f"Error: {e.message}")
        imap.logout()
