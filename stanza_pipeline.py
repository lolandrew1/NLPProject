
import stanza

stanza.download('en') # download English model
nlp = stanza.Pipeline('en') # initialize English neural pipeline

def tag(lines):
  tags = nlp(lines)
  return tags