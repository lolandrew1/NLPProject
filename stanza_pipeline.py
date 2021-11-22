
import stanza

stanza.download('en') # download English model
nlp = stanza.Pipeline('en') # initialize English neural pipeline

def tag(lines):
  tag = (nlp(line) for line in lines)

  return tag