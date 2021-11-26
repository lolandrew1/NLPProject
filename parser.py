
from bs4 import BeautifulSoup

def parse_file(filename):
  file = open(filename)
  soup = BeautifulSoup(file, features="html.parser")

  text = soup.get_text()
  lines = (line.strip() for line in text.splitlines() if len(line) > 20)
  text = ' '.join(lines)

  return text