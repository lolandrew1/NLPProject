
import sys  
import parser
import stanza_pipeline

file = sys.argv[1]
numQs = int(sys.argv[2])
user = sys.argv[3]

lines = parser.parse_file(file)

# documentation on tags: https://stanfordnlp.github.io/stanza/data_objects.html#sentence

binQs = stanza_pipeline.getQs(lines)

for binQ in binQs:
  print(binQ)







