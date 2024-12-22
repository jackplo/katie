import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class CredentialsManager:
  _credentials_file = "token.json"
    
  @classmethod
  def initialize(cls, scopes):
    if os.path.exists(cls._credentials_file):
      creds = Credentials.from_authorized_user_file(cls._credentials_file, scopes)
    else:
      creds = None

    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", scopes
        )
        creds = flow.run_local_server(port=0)
        
      with open(cls._credentials_file, "w") as token:
        token.write(creds.to_json())
            
    return creds
  
  @classmethod
  def get_credentials(cls, scopes):
    if not os.path.exists(cls._credentials_file):
      raise RuntimeError("Credentials not initialized. Run main.py first.")
        
    creds = Credentials.from_authorized_user_file(cls._credentials_file, scopes)
    
    if creds.expired and creds.refresh_token:
      creds.refresh(Request())
      with open(cls._credentials_file, "w") as token:
        token.write(creds.to_json())
            
    return creds