import sys  
import os.path
import fine_tune
from transformers import DistilBertTokenizerFast
from transformers import DistilBertForQuestionAnswering
from transformers import pipeline

context_file = sys.argv[1]
question_file = sys.argv[2]

f = open(question_file, "r", encoding="utf8")
questions = f.read().split("\n")
f.close()

f = open(context_file, "r", encoding="utf8")
context = f.read()
f.close()


if os.path.exists("models/distilbert-custom"):
    model = DistilBertForQuestionAnswering.from_pretrained("models/distilbert-custom")
else:
    model = fine_tune.tune()

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

nlp = pipeline("question-answering", model = model, tokenizer = tokenizer)

for i in range(len(questions)):
    res = nlp({"question" : questions[i], "context" : context})
    
    print("A" + str(i) + ": " + context[res["start"]:res["end"]])
    
