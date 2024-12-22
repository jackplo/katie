from katie.utils.constants.scopes import SCOPES
from katie.managers.credentials_manager import CredentialsManager
from celery_config import celery_app

def main():
  print("Starting katie...")
  CredentialsManager.initialize(SCOPES)
  print("Katie is connected and running...")
  
if __name__ == '__main__':
  main()