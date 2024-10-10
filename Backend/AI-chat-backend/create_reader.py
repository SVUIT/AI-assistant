from transformers import pipeline
# load the reader model into a question-answering pipeline
model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
reader = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad", device=-1)