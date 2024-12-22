from celery_config import celery_app
from googleapiclient.discovery import build
from katie.utils.constants.scopes import SCOPES
from katie.managers.credentials_manager import CredentialsManager
from katie.models.email_classifier import EmailClassifier
from katie.utils.helpers.decode_email_contents import decode_email_contents

@celery_app.task
def fetch_emails():
  try:
    creds = CredentialsManager.get_credentials(SCOPES)
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId = "me", maxResults=50, q="newer_than:1d AND category:primary AND is:unread").execute()

    if results['resultSizeEstimate'] == 0:
      print("No labels found.")
      return

    messages = results["messages"]
    emails = []

    for message in messages:
      message_id = message["id"]
      email_raw_data = service.users().messages().get(userId = "me", id=message_id, format="raw").execute()
      email = decode_email_contents(email_raw_data)
      emails.append(email)

    # Classify by AI

    

  except Exception as e:
    print(f"An error occurred while fetching emails...\n{e}")
