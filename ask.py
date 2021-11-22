
import sys  
import parser
import stanza_pipeline

file = sys.argv[1]
numQs = int(sys.argv[2])
user = sys.argv[3]

lines = parser.parse_file(file)

tags = stanza_pipeline.tag(lines)

for tag in tags:
  print(tag)






