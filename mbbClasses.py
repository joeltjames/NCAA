import MBB
import scraperUtils

class TeamNameError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return "Error no team found with name: " + repr(self.value)

class Player(object):
    first_name = ""
    last_name = ""
    rest = ""

class TeamSeason(object):
    # a team stats for a single season
    ncaa_id = -1
    end_year = 1900
    roster = []

    def __lt__(self,o):
        return self.end_year < o.end_year

class Team(object):
    # a generic team class
    ncaa_id = -1
    name = ""
    indiviualSeasons = []

    def __init__(self,name,ncaa_id):
        self.name = name
        self.ncaa_id = ncaa_id
        self.url = "http://stats.ncaa.org/team/index/%s?org_id=" + str(ncaa_id)
        self.indiviualSeasons = MBB.getSeasonsData(self)
        self.roster = list(reversed(sorted(self.indiviualSeasons)))[0] #.roster


    def getUrl(self,season_id=None):
        if season_id is None:
            return self.url % '12020'
        else:
            return self.url % season_id

    def __str__(self):
        return self.name

class TeamSchedule(object):
    ncaa_id = -1
    games = []

class Game(object):
    home_team = -1
    away_team = -1