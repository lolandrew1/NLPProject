import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup

def read(filename):
    return pd.read_csv(filename, encoding='ISO-8859-1')

#Taken from https://hackersandslackers.com/scraping-urls-with-beautifulsoup/
def get_html(link):
    headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    req = requests.get(link, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup
    

def parse_file(soup):
  text = soup.get_text()
  lines = (line.strip() for line in text.splitlines() if len(line) > 20)
  text = ' '.join(lines)

  return text

def get_data_lists(data):
    data = read(data)

    links = {}

    questions = []
    contexts = []
    answers = []

    for index, row in data.iterrows():
        works = True
        if (row["wiki-url"] in links):
            contexts.append(str(links[row["wiki-url"]]))
        else:
            try:
                txt = parse_file(get_html((str(row["wiki-url"]))))
                links[row["wiki-url"]] = txt
                contexts.append(txt)
            except:
                works = False

        if works:
            questions.append(str(row['question']))
            answers.append(str(row["answer 1"]))
    return questions, contexts, answers

def get_data(data):
    questions, contexts, answers = get_data_lists(data)

    answer_dict_list = []
    new_q = []
    new_a = []
    new_c = []

    for ans in range(len(answers)):
        if answers[ans].lower() == "no" or answers[ans].lower() == "yes":
            continue
        pos = contexts[ans].find(answers[ans])
        if pos == -1:
            continue
        else:
            answer_dict = {}
            answer_dict["answer"] = answers[ans]
            answer_dict['answer_start'] = pos
            answer_dict['answer_end'] = pos + len(answers[ans])
            answer_dict_list.append(answer_dict)
            new_q.append(questions[ans])
            new_a.append(answers[ans])
            new_c.append(contexts[ans])
    '''
    contexts is the list of contexts, questions is the list of questions
    answers is the list of answers
    answer_dict_list is the list of dictionaries where 'answer' is the actual answer
    'answer_start' is the starting index of the answer in the context
    and 'answer_end' is the ending index of the answer in the context
    '''
    return new_c, new_q, new_a, answer_dict_list

'''
info = get_data("data.csv")
contexts = info[0]
questions = info[1]
answers = info[2]
answer_dict_list = info[3]

print(len(contexts), len(questions), len(answers), len(answer_dict_list))
'''     
        
            










    

