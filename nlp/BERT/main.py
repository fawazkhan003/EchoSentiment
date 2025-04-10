from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import re

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

statement = ''
tokens = tokenizer.encode(statement, return_tensors='pt')

result = model(tokens)

value = int(torch.argmax(result.logits)) + 1

if value < 3:
    sentiment = 'Negative'
elif value > 3:
    sentiment = 'Positive'
else:
    sentiment = 'Neutral'

print(sentiment)
