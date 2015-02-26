from scraperUtils import getSoup
import mbbUtils
from bs4 import BeautifulSoup
from pprint import pformat

base_url = mbbUtils.getUrl()
seasonCodes = mbbUtils.getSeasonCodesList()

teamNameCodeDict = dict()
for i in range(0,2000):
    if i % 100 == 0:
        print(i)
    for code in seasonCodes:
        thisUrl = base_url.format(code,str(i))
        soup = getSoup(thisUrl)
        header = soup.h1.text.strip()
        if "(" in header:
            parts = header.split("(")
            teamName = parts[0].strip()
            teamNameCodeDict[teamName] = i
            break

with open("teamCodes.dat", "w+") as f:
    data = pformat(teamNameCodeDict)
    f.write(data)