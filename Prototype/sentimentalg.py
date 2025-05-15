from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
def analyze_sentiment(text):
    if not text.strip():
        return "Neutral"  # Handle empty strings

    tokens = tokenizer.encode(text, return_tensors='pt', truncation=True, max_length=512)
    result = model(tokens)
    value = int(torch.argmax(result.logits)) + 1  # Ratings are 1 to 5

    if value < 3:
        return 'Negative'
    elif value > 3:
        return 'Positive'
    else:
        return 'Neutral'
