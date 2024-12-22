from transformers import pipeline

class EmailClassifier:
  classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

  @classmethod
  def classify_string_contents(self, string, classifications):
    result = self.classifier(string, classifications)
    predicted_label = result['labels'][result['scores'].index(max(result['scores']))]
    return predicted_label
  
  @classmethod
  def classify_sender_type(self, sender_email):
    classifications = ["Advertisement", "Social Media", "News"]