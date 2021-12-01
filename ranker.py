
def compfn(question):
  return len(question)

def rank(questions, numQs):
  sortedQs = sorted(questions, key=compfn)
  if numQs <= len(sortedQs):
    return sortedQs[:numQs]
  else:
    numDummyQs = numQs - len(sortedQs)
    dummyQs = ["No more questions :,("] * numDummyQs
    return sortedQs + dummyQs