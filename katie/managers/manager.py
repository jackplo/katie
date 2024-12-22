from abc import ABC, abstractmethod

class Manager(ABC):

  def __init__(self, celery_app):
    self.celery_app = celery_app

  @abstractmethod
  def connect(self):
    pass

  @abstractmethod
  def start_tasks(self):
    pass

  @abstractmethod
  def disconnect(self):
    pass
    
  

  
