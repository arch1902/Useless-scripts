# Author : ARPIT CHAUHAN 
# Entry Number : 2019CS10332

from bs4 import BeautifulSoup
from urllib2 import urlopen
import re

PEOPLE = ["Bill_Gates", "Elon_Musk", "Narendra_Modi", "Sachin_Tendulkar", "Donald_Trump",
          "Ratan_Tata", "Jeff_Bezos", "Barack_Obama", "Mark_Zuckerberg", "Mukesh_Ambani"]



WIKI_URL = "https://en.wikipedia.org/wiki/"
SOURCE_URL = "https://en.wikipedia.org/w/index.php?title={}&action=edit"

endPattern = re.compile("\n}}\n")


def generateId(str):
    return str.replace(" ", "_")


def readEvents(soup, events):
    for event in events:
        print(event.string)
        id = generateId(event.string)
        header = soup.find("span", {"id": id})
        para = header.parent.find_next('p')
        for content in para.contents:
            print(content.string)


def tryMatch(data):
    for possiblePattern in ["{{Infobox cricketer", "{{Infobox officeholder", "{{Infobox person", "{{infobox person"]:
        try:
            return data.index(possiblePattern) + len(possiblePattern)
        except:
            pass


def beautifyData(data):
    data = data.replace("<br>", "")
    data = re.sub("<br.*/>", "", data)
    data = re.sub(".*image.*=.*", "", data)
    data = re.sub("<!--.*-->", "", data)
    data = re.sub("<ref.*/ref>", "", data)
    data = re.sub("\|{{url\|.*}}\|", "", data)
    data = data.replace("|", "")
    return data


def getIndexOfMatch(data, pattern):
    for m in re.finditer(pattern,  data):
        return (m.span()[0])


def readProperties(soup, textarea):
    content = textarea.string
    beginIndex = tryMatch(content)
    endIndex = beginIndex + getIndexOfMatch(content[beginIndex:], endPattern)
    keyValueContent = content[beginIndex:endIndex]
    print(beautifyData(keyValueContent))


for famousPerson in PEOPLE:
    print("\n\n##########  Learning about " +
          famousPerson + "    ##############")
    personalUrl = WIKI_URL + famousPerson
    sourceUrl = SOURCE_URL.format(famousPerson)
    page = urlopen(sourceUrl)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    readProperties(soup, soup.find("textarea", {"id": "wpTextbox1"}))
    # readEvents(soup, soup.findAll("span", {"class": "toctext"}))
