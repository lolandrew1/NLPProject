import read
from transformers import DistilBertTokenizerFast

global tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

def tokenize():
    global tokenizer
    train_contexts, train_questions, train_answers, train_answers_dict = read.get_data("data.csv")
    train_encodings = tokenizer(train_contexts, train_questions, truncation = True, padding = True)
    return train_encodings, train_answers_dict 

def add_positions(encodings, answer_indicies):
    global tokenizer

    start_indicies = []
    end_indicies = []
    for i in range(len(answer_indicies)):
        start_add = encodings.char_to_token(i, answer_indicies[i]['answer_start'])
        end_add = encodings.char_to_token(i, answer_indicies[i]['answer_end'])

        if not start_add:
            start_indicies.append(tokenizer.model_max_length)
        else:
            start_indicies.append(start_add)
        
        minus = 1
        while not end_add:
            end_add = encodings.char_to_token(i, answer_indicies[i]['answer_end']-minus)
            minus +=1
        end_indicies.append(end_add)

    encodings.update({'start_positions': start_indicies, 'end_positions': end_indicies})

'''
train_encodings, answers = tokenize()

add_positions(train_encodings, answers)

print(train_encodings.keys())
'''