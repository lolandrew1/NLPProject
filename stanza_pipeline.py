
import stanza
from stanza.server import CoreNLPClient

stanza.download('en') # download English model
nlp = stanza.Pipeline('en') # initialize English neural pipeline

with CoreNLPClient(
        annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse'],
        timeout=300000,
        memory='16G') as client:


  # create a single binary, auxiliary question 
  # given a NP and VP
  def makeBinQ(NPP, VPP):
    VP = processTree(nlp(VPP).sentences[0].constituency)

    firstVerb = getFirstVerb(VP).capitalize()
    restVP = VP.children[1:] if len(VP.children) > 1 else []

    firstVerbProcessed = (nlp(firstVerb)).sentences[0].words[0]
    firstVerbLemma = firstVerbProcessed.lemma
    
    # determine if the verb is an auxiliary verb
    if firstVerbLemma == "be":
      NP = nlp(NPP).sentences[0]
      words = NP.words
      nounType = typeOfNoun(words)  

      # the NP is characterized by a proper noun
      if nounType == 1:
        return (' '.join([firstVerb, NPP, childrenToString(restVP)])) + "?"
      elif nounType == 2:
        NPP = NPP[0].lower() + NPP[1:]
        return (' '.join([firstVerb, NPP, childrenToString(restVP)])) + "?" 

   
    # otherwise if the sentence is characterized by a pronoun
    # we don't add it to the list of questions
    return ""

  # makes Wh-question by replacing NP with Wh-word
  def makeWhQ(NPP, VPP):
    NP = nlp(NPP).sentences[0]
    tokens = NP.tokens
    words = NP.words
    WhWord = getWhWord(tokens, words)
    return (WhWord + " " + VPP + "?")

  # returns a list of binary questions (yes or no questions)
  def getQs(text):
    # find a phrase with a NP that is the immediate sibling
    # of a VP which has some form of a VB as the left-most
    # word
    patternNP = "NP $+ (VP <<, /VB.?/)"
    patternVP = "(VP <<, /VB.?/) $- NP"

    # The NP part of the phrase
    NPmatches = client.tregex(text, patternNP)
    # The VP part of the phrase
    VPmatches = client.tregex(text, patternVP)
    
    # Binary Questions
    binQs = getBinQs(NPmatches, VPmatches)
    # Wh-Questions
    whQs = getWhQs(NPmatches, VPmatches)

    # combine the two types of questions
    return (binQs + whQs)

  # returns binary, auxiliary questions
  def getBinQs(NPmatches, VPmatches):
    qs = []
    for i in range(len(NPmatches['sentences'])):
      for j in range(len(NPmatches['sentences'][i]) > 0):
        NP = NPmatches['sentences'][i][str(j)]["spanString"]
        VP = VPmatches['sentences'][i][str(j)]["spanString"]
        q = makeBinQ(NP, VP)
        if len(q) > 1:
          qs.append(q)

    return qs

  # returns Wh-questions
  def getWhQs(NPmatches, VPmatches):
    qs = []
    for i in range(len(NPmatches['sentences'])):
      for j in range(len(NPmatches['sentences'][i]) > 0):
        NP = NPmatches['sentences'][i][str(j)]["spanString"]
        VP = VPmatches['sentences'][i][str(j)]["spanString"]
        q = makeWhQ(NP, VP)
        if len(q) > 1:
          qs.append(q)

    return qs

  # helper functions -----------------------------------------

  # gets the first verb of a VP and returns it as a string
  def getFirstVerb(VP):
    while len(VP.children) != 0:
      VP = VP.children[0]
    return str(VP)

  # determines what type of noun characterizes the NP
  def typeOfNoun(words):
    for word in words:
      if word.upos == "PROPN":
        return 1
      elif word.upos == "PRON":
        return 3
      elif word.upos == "NOUN":
        return 2
    return 3

  # finds corresponding Wh-word for NP
  def getWhWord(tokens, words):
    for i in range(len(tokens)):
      word = words[i]
      token = tokens[i]

      if word.upos == "PROPN":
        if token.ner == "S-PERSON":
          return "Who"
        else:
          return "What"
      elif word.upos  == "NOUN" or word.lemma == "it":
        return "What"
      elif word.upos  == "PRON":
        return "Who"
    
    return "What"
      

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

  # returns a parseTree with VP and NP children
  def processTree(tree):
    while tree.label == 'S' or tree.label == 'ROOT':
      tree = tree.children[0]
    return tree

      
