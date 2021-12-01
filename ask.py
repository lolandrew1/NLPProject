
import sys  
import parser
import stanza_pipeline
import ranker

file = sys.argv[1]
numQs = int(sys.argv[2])

lines = parser.parse_file(file)

questions = stanza_pipeline.getQs(lines)

finalQuestions = ranker.rank(questions, numQs)

for question in finalQuestions:
  print(question)










