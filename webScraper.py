from bs4 import BeautifulSoup
from color import get_coloredText
import requests


class WebScraper():
    def __init__(self, url):
        self.url = url
        self.parseDataIntoSoup()

    
    def parseDataIntoSoup(self):
        req = requests.get(self.url)
        htmlData = req.text
        soup = BeautifulSoup(htmlData, 'html.parser')
        self.soup = soup
       

    def printDataByP(self):
        for item in self.soup.findAll("p"):
            print(item.text)

class NFL_Team_WebScraper(WebScraper):
    def __init__(self, url):
        super().__init__(url)
    
    def printAllTeams(self):
        teams = []
        for i,item in enumerate(self.soup.findAll("p")):
            if i < 32:
                teams.append(item.text)
        print(teams)

    def getTeamList(self):
        teams = []
        for i,item in enumerate(self.soup.findAll("p")):
            if i < 32:
                name = item.text.lower().split()
                teamName=''
                for word in name:
                    if teamName == "":
                        teamName = word
                    else:
                        teamName += f'-{word}'
                teams.append(teamName)
        return teams

class NFL_Stat_WebScraper(WebScraper):
    def __init__(self, url):
        super().__init__(url)

    def parseData(self):
        data = []
        for line,item in enumerate(self.soup.findAll("div")):
            if line ==15 :
                data.append(item.text)
            if line > 32:
                data.append(item.text)
                #print(f'Line Number  :{i}')
        return data


class SideOfTeam():
    def __init__(self, side):
        self.side = side

    def handleSingleStats(self,stats):
        self.totalFirstDowns = stats[0]
        self.totalOffensiveYards = stats[1]
        self.totalRushingYards = stats[2]
        self.totalPassingYards = stats[3]
        self.sacks = stats[4]
        self.touchdowns = stats[5]

class Team():
    def __init__(self,data):
        self.data = data
        
        self.offense = SideOfTeam("Offense")
        self.defense = SideOfTeam("Defense")
        self.handleData()
        
    def handleData(self):
       # print(f'Category        For     Against')
        temp = []
        offenseSingleStats = []
        defenseSingleStats = []
        self.name = self.data[0]
        self.data.pop(0)
        for i,div in enumerate(self.data):  
            if i <=49:
                if i % 3 == 0 and len(temp) >0:
                    #print(f'{i} ){temp[1]} : {temp[0]}   {temp[2]}')
                    
                    try:
                        int(temp[0])
                        int(temp[2])
                        #print(f'CATEGORY : {temp[1]}[{i-1}]')
                        #print(f'Offense: {temp[0]} [{i-2}] Defense:{temp[2]} [{i}]')
                        offenseSingleStats.append(temp[0])
                        defenseSingleStats.append(temp[2])
                    except ValueError:
                        a = 2
                        #print(f"MORE THAN ONE CATEGORY ({temp[1]} [{i-1}]")
                    temp = [] 
                    temp.append(div)
                else: 
                    temp.append(div)
        self.offense.handleSingleStats(offenseSingleStats)
        self.defense.handleSingleStats(defenseSingleStats)    

    def showBroadData(self):
        dashedLine = get_coloredText("==================================================","red", True)
        print(dashedLine)
        print(f'Team Name:      {self.name}')
        print('Category                 Off.    Def.')
        print(f'Total First Downs       {self.offense.totalFirstDowns}  {self.defense.totalFirstDowns}')
        print(f'Total Offenseie Yards   {self.offense.totalOffensiveYards}  {self.defense.totalOffensiveYards}')
        print(f'Total Rushing Yards     {self.offense.totalRushingYards}  {self.defense.totalRushingYards}')
        print(f'Total Passing Yards     {self.offense.totalPassingYards}  {self.defense.totalPassingYards}')
        print(f'Total Sacks             {self.offense.sacks}  {self.defense.sacks}')
        print(f'Total Touchdowns        {self.offense.touchdowns}   {self.defense.touchdowns}')

TeamScraper = NFL_Team_WebScraper("https://nfl.com/teams")
teams = TeamScraper.getTeamList()


def getDataFromAllTeams():
    for team in teams:
        StatScraper = NFL_Stat_WebScraper(f"https://nfl.com/teams/{team}/stats")
        teamData = StatScraper.parseData()

        tempTeam = Team(teamData)
        tempTeam.showBroadData()

getDataFromAllTeams()