
import stanza

stanza.download('en') # download English model
nlp = stanza.Pipeline('en') # initialize English neural pipeline

def tag(lines):
  tags = nlp(lines)
  return tags

def isBinQ(sentence):
  parseTree = sentence.constituency
  sent = parseTree.children[0].children

  return sent[0].label == "NP" and sent[1].label == "VP"

def makeBinQ(sentence):
  parseTree = sentence.constituency
  sent = parseTree.children[0].children
  NP = sent[0]
  VP = sent[1]
  firstVerb = getFirstVerb(VP).capitalize()
  restVP = VP.children[1:] if len(VP.children) > 1 else []

  firstVerbProcessed = (nlp(firstVerb)).sentences[0].words[0]
  firstVerbLemma = firstVerbProcessed.lemma
  
  if firstVerbLemma == "be":
    # in this case we move the firstverb to the front of the sentence
    return (' '.join([firstVerb, treeToString(NP), childrenToString(restVP)])) + "?"
  else:
    # in this case we simply append "Is it true that" to the sentence
    return ("Is it true that " + sentence.text + "?")
  

# returns a list of binary questions (yes or no questions)
def getBinQs(doc):
  binQs = []
  for sentence in doc.sentences:
    if isBinQ(sentence):
      binQs.append(makeBinQ(sentence))

  return binQs
  

# helper functions -----------------------------------------

# gets the first verb of a VP and returns it as a string
def getFirstVerb(VP):
  while len(VP.children) != 0:
    VP = VP.children[0]
  return str(VP)

# concats the children of parseTree node into one string
def childrenToString(children):
  words = []
  for child in children:
    words.append(treeToString(child))
  
  return ' '.join(words)

# converts parseTree to string
def treeToString(tree):
  if len(tree.children) == 0:
    return str(tree)
  else:
    words = []
    for child in tree.children:
      words.append(treeToString(child))
    
    return ' '.join(words)