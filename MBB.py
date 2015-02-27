import scraperUtils
import mbbClasses

def getUrl(season_id=None,team_id=None):
    base_url = "http://stats.ncaa.org/team/index/{0}?org_id={1}"
    if not (season_id is None) and not (team_id is None):
        base_url = base_url.format(season_id,team_id)
    return "http://stats.ncaa.org/team/index/{0}?org_id={1}"

def getEndYear(season_id):
    if str(season_id).strip() == "10260":
        return 2010
    if str(season_id).strip() == "10440":
        return 2011
    if str(season_id).strip() == "10740":
        return 2012
    if str(season_id).strip() == "11220":
        return 2013
    if str(season_id).strip() == "11540":
        return 2014
    if str(season_id).strip() == "12020":
        return 2015

def getRosterUrl(season_id,team_id):
    return "http://stats.ncaa.org/team/roster/%s?org_id=%s" % (season_id, team_id)

def getPlayerStatsUrl(season_id, team_id):
    return  "http://stats.ncaa.org/team/stats?org_id=%s&sport_year_ctl_id=%s" % (team_id,season_id)

def getTeamUrl(team_id):
    return "http://stats.ncaa.org/team/index/12020?org_id=%s" % (team_id)

def getSeasonCodesDict():
    return {"09-10":10260, "10-11":10440, "11-12":10740, "12-13":11220, 
            "13-14":11540,"14-15":12020}

def getSeasonCodesList():
    return [10260,10440,10740,11220,11540,12020]

def getTeamCodesDict():
    return {u'Menlo Oaks': 405, u'Mercer Bears': 406}

def getFloat(value, default=0.0):
    try: 
        return float(value)
    except: 
        return 0.0


def getInteger(value, default=0.0):
    try:
        return int(value)
    except:
        return 0

def getPlayerStats(roster, season_id, team_id):
    player_stats_url = getPlayerStatsUrl(season_id, team_id)
    soup = scraperUtils.getSoup(player_stats_url)
    table = soup.find("table", {"id" :"stat_grid"})
    for row in table.findAll("tr"):
        if row.get('class',[''])[0] == 'grey_heading':
            continue  
        cell_data = [x.find(text=True) for x in row.findAll("td")]
        player_number = str(cell_data[0])
        if player_number == "-":
            continue
        this_player = next(x for x in roster if x.number == player_number)
        minutes_parts = [float(str(x).strip()) for x in cell_data[7].strip().split(":")]
        this_player.minutes_played = minutes_parts [0] + (minutes_parts[1] / 60.0)
        
        this_player.field_goals_made = getFloat(cell_data[8])
        this_player.field_goals_attempted = getFloat(cell_data[9])        
        if this_player.field_goals_attempted == 0.0:
            this_player.field_goal_percentage = 0.0
        else:
            this_player.field_goal_percentage = 100.0 * (this_player.field_goals_made / this_player.field_goals_attempted)

        this_player.three_pointers_made = getFloat(cell_data[11])
        this_player.three_pointers_attempted = getFloat(cell_data[12])
        if this_player.three_pointers_attempted == 0.0:
            this_player.three_point_percentage = 0.0
        else:
            this_player.three_point_percentage = 100.0 * (this_player.three_pointers_made / this_player.three_pointers_attempted)

        this_player.free_throws_made = getFloat(cell_data[14])
        this_player.free_throws_attempted = getFloat(cell_data[15])
        if this_player.free_throws_attempted == 0:
            this_player.free_throw_percentage = 0.0
        else:
            this_player.free_throw_percentage = this_player.free_throws_made / this_player.free_throws_attempted

        this_player.total_points = getInteger(cell_data[17])
        this_player.average_points = this_player.total_points / this_player.games_played
        this_player.offensive_rebounds = getInteger(cell_data[19])        
        this_player.defensive_rebounds = getInteger(cell_data[19])
        this_player.total_rebounds = this_player.offensive_rebounds + this_player.defensive_rebounds
        this_player.average_rebounds = this_player.total_rebounds / this_player.games_played
        this_player.assists = getInteger(cell_data[23])
        this_player.turnovers = getInteger(cell_data[24])
        this_player.steals = getInteger(cell_data[25])
        this_player.blocks = getInteger(cell_data[26])
        this_player.fouls = getInteger(cell_data[27])
        this_player.double_doubles = getInteger(cell_data[28])
        this_player.triple_doubles = getInteger(cell_data[29])
        if len(cell_data) > 30:        
            this_player.disqualifications = getInteger(cell_data[30])
        else:
            this_player.disqualifications = 0
    return roster

def getRoster(season_id, team_id):
    roster_url = getRosterUrl(season_id, team_id)
    soup = scraperUtils.getSoup(roster_url)
    print(soup)
    table = soup.find("table", {"id" :"stat_grid"})
    roster = []
    for row in table.findAll("tr"):
        if row.get('class',[''])[0] == 'heading':
            continue        
        cell_data = [x.find(text=True) for x in row.findAll("td")]
        this_player = mbbClasses.Player()
        this_player.number = str(cell_data[0])
        name_parts = [str(x.strip()) for x in cell_data[1].split(",")]
        if len(name_parts) == 2:
            this_player.last_name, this_player.first_name = name_parts
        else:
            this_player.last_name, this_player.rest, this_player.first_name = name_parts
        this_player.position = cell_data[2]
        if len(cell_data[3]) > 1:
            height_parts = [int(x.strip()) for x in cell_data[3].strip().split("-")]
            this_player.height = height_parts[0] * 12 + height_parts[0]
        else:
            this_player.height = -1
        this_player.year = cell_data[4]
        this_player.games_played = getInteger(cell_data[5])
        this_player.games_started = getInteger(cell_data[6])
        roster.append(this_player)
    return getPlayerStats(roster, season_id, team_id)

def getSeasonStats(season):
    stats_url = getPlayerStatsUrl(season.season_id, season.ncaa_id)
    soup = scraperUtils.getSoup(stats_url)
    table = soup.find("table", {"id" :"stat_grid"})
    rows = table.findAll("tr")
    reversed_rows = list(reversed(rows))    
    season.total_games = max([x.games_played for x in season.roster])
    defensive_totals = [x.find(text=True) for x in reversed_rows[0].findAll("td")]
    offensive_totals = [x.find(text=True) for x in reversed_rows[1].findAll("td")]

    season.opponent_field_goals_made = getFloat(defensive_totals[8])    
    season.opponent_field_goals_attempted = getFloat(defensive_totals[9])
    if season.opponent_field_goals_attempted == 0:
        season.opponent_field_goal_percentage = 0.0
    else:
        season.opponent_field_goal_percentage = 100.0 * (season.opponent_field_goals_made / season.opponent_field_goals_attempted)

    season.opponent_three_pointers_made = getFloat(defensive_totals[11])    
    season.opponent_three_pointers_attempted = getFloat(defensive_totals[12])
    if season.opponent_three_pointers_attempted == 0:
        season.opponent_three_point_percentage = 0.0
    else:
        season.opponent_three_point_percentage = 100.0 * (season.opponent_three_pointers_made / season.opponent_three_pointers_attempted)

    season.opponent_free_throws_made = getFloat(defensive_totals[11])    
    season.opponent_free_throws_attempted = getFloat(defensive_totals[12])
    if season.opponent_free_throws_attempted == 0:
        season.opponent_free_throw_percentage = 0.0
    else:
        season.opponent_free_throw_percentage = 100.0 * (season.opponent_free_throws_made / season.opponent_free_throws_attempted)

    season.opponent_points = getInteger(defensive_totals[14])
    season.opponent_points_per_game = season.opponent_points / season.total_games
    season.opponent_offensive_rebounds = getInteger(defensive_totals[16])
    season.opponent_defensive_rebounds = getInteger(defensive_totals[17])
    season.opponent_total_rebounds = season.opponent_offensive_rebounds + season.opponent_defensive_rebounds
    season.opponent_offensive_rebounds_per_game = season.opponent_offensive_rebounds / season.total_games
    season.opponent_defensive_rebounds_per_game = season.opponent_defensive_rebounds / season.total_games
    season.opponent_assists = getInteger(defensive_totals[18])
    season.opponent_steals = getInteger(defensive_totals[19])
    season.opponent_turnovers = getInteger(defensive_totals[19])
    season.opponent_blocks = getInteger(defensive_totals[19])
    season.opponent_fouls = getInteger(defensive_totals[19])
    
    
    season.field_goals_made = getFloat(offensive_totals[8])    
    season.field_goals_attempted = getFloat(offensive_totals[9])
    if season.field_goals_attempted == 0:
        season.field_goal_percentage = 0.0
    else:
        season.field_goal_percentage = 100.0 * (season.field_goals_made / season.field_goals_attempted)

    season.three_pointers_made = getFloat(offensive_totals[11])    
    season.three_pointers_attempted = getFloat(offensive_totals[12])
    if season.three_pointers_attempted == 0:
        season.three_point_percentage = 0.0
    else:
        season.three_point_percentage = 100.0 * (season.three_pointers_made / season.three_pointers_attempted)

    season.free_throws_made = getFloat(offensive_totals[11])    
    season.free_throws_attempted = getFloat(offensive_totals[12])
    if season.free_throws_attempted == 0:
        season.free_throw_percentage = 0.0
    else:
        season.free_throw_percentage = 100.0 * (season.free_throws_made / season.free_throws_attempted)

    season.points = getInteger(offensive_totals[14])
    season.points_per_game = season.points / season.total_games
    season.offensive_rebounds = getInteger(offensive_totals[16])
    season.defensive_rebounds = getInteger(offensive_totals[17])
    season.total_rebounds = season.offensive_rebounds + season.defensive_rebounds
    season.offensive_rebounds_per_game = season.offensive_rebounds / season.total_games
    season.defensive_rebounds_per_game = season.defensive_rebounds / season.total_games
    season.assists = getInteger(offensive_totals[18])
    season.steals = getInteger(offensive_totals[19])
    season.turnovers = getInteger(offensive_totals[19])
    season.blocks = getInteger(offensive_totals[19])
    season.fouls = getInteger(offensive_totals[19])

def getSchedule(season_id, team_id):
    schedule_url = getUrl(season_id, team_id)
    soup = scraperUtils.getSoup(schedule_url)
    table = soup.find("table", {"class" :"mytable"})
    print(soup)
    schedule = []
    for row in table.findAll("tr"):        
        if row.get('class',[''])[0] == 'grey_heading':
            continue
        cell_data = [x.find(text=True) for x in row.findAll("td")]
        thisGame = MBB.Game()
        thisGame.date = cell_data[0]

def getSeasonData(season_id,team_id):
    this_season = mbbClasses.TeamSeason(season_id,team_id,getEndYear(season_id))
    this_season.roster = getRoster(season_id, team_id)
    getSeasonStats(this_season)
    this_season.schedule = getSchedule(season_id, team_id)
    return this_season

def getSeasonsData(team):
    seasonsData = []
    for code in getSeasonCodesList():
        seasonsData.append(getSeasonData(code, team.ncaa_id))
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