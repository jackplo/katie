import base64
import email
import email.policy
from bs4 import BeautifulSoup
import re

def clean_text(content):
  cleaned_content = re.sub(r'\s*\n\s*', '\n', content)
  cleaned_content = re.sub(r'\n{2,}', '\n', cleaned_content)
  return cleaned_content.strip()

def safe_decode(payload):
  try:
    return payload.decode("utf-8")
  except UnicodeDecodeError:
    try:
      return payload.decode("iso-8859-1")
    except UnicodeDecodeError:
      return "[Content not decodable]"

def decode_email_contents(raw_email):
  email_content_b64_encoded = raw_email["raw"]
  email_content_mime_encoded = base64.urlsafe_b64decode(email_content_b64_encoded)
  email_content = email.message_from_bytes(email_content_mime_encoded)
  
  return get_text_from_parsed_email(email_content)

def get_text_from_parsed_email(msg):

  text_content = []

  if msg.is_multipart():
    for part in msg.get_payload():
      text_content.append(get_text_from_parsed_email(part))
  else:
    content_type = msg.get_content_type()
    if content_type == "text/plain":
      text_content.append(safe_decode(msg.get_payload(decode=True)))
    elif content_type == "text/html":
      html_content = safe_decode(msg.get_payload(decode=True))
      text_content.append(BeautifulSoup(html_content, "html.parser").get_text())

  message = " ".join(filter(None, text_content)).strip()
  cleaned_message = clean_text(message)
  return cleaned_message