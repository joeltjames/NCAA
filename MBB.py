import scraperUtils
import mbbClasses

def getUrl(season_id=None,team_id=None):
    base_url = "http://stats.ncaa.org/team/index/{0}?org_id={1}"
    if not (season_id is None) and not (team_id is None):
        base_url = base_url.format(season_id,team_id)
    return "http://stats.ncaa.org/team/index/{0}?org_id={1}"

def getTeamUrl(team_id):
    return "http://stats.ncaa.org/team/index/12020?org_id=%s" % (team_id)

def getSeasonCodesDict():
    return {"09-10":10260, "10-11":10440, "11-12":10740, "12-13":11220, 
            "13-14":11540,"14-15":12020}

def getSeasonCodesList():
    return [10260,10440,10740,11220,11540,12020]

def getTeamCodesDict():
    return {u'Menlo Oaks': 405, u'Mercer Bears': 406}

def getSeasonData(url):
    soup = scraperUtils.getSoup(url)

def getSeasonsData(team):
    seasonsData = [3,2,1]
    for code in getSeasonCodesList():
        season_url = team.getUrl(code)
        print(season_url)
    return seasonsData


def getTeamCode(team_name):    
    team_codes = getTeamCodesDict()
    
    if team_name in team_codes:
        return team_codes[team_name]
    else:
        raise Exception(team_name + " not found in team list.")

def getTeam(name):
    ncaa_id = getTeamCode(name) 
    team = mbbClasses.Team(name, ncaa_id)
    return team