import urllib.request
import json


def printAllTeamsInLeague(countryName, leagueName):
    """Simply prints out all teams in a specific league to the terminal """

    leagueID = getLeagueID(countryName, leagueName)

    rec = urllib.request.Request("https://api-football-v1.p.rapidapi.com/v2/teams/league/" + str(leagueID))

    rec.add_header("X-RapidAPI-Host", "api-football-v1.p.rapidapi.com")
    rec.add_header("X-RapidAPI-Key", "1acHO5cH5QmshrLw9WFJXPxKPIgEp1uE4YzjsnGOydel9eubG9")

    with urllib.request.urlopen(rec) as response:
        #print("Status code from response: {}".format(response.getcode()))
        #print("Status code from response: {}".format(response.getheaders()))
        decodedTeams = response.read()
    
        teams = json.loads(decodedTeams, encoding = "utf-8")    

        for team in teams["api"]["teams"]:
            print(team["name"])


def saveAsJSON(dictionary):
    with open("leagues.json", "w") as leagueFile:
        json.dump(dictionary, leagueFile)


def getLeagueID(countryName, leagueName):
    """Finds the league ID of a league. By defualt it will return the current live league(2019)"""

    with open("leagues.json", "r") as leagueFile:
        leagues = json.load(leagueFile)["api"]["leagues"]
        for league in leagues:
            if (league["country"] == countryName and league["season"] == 2019 and league["name"] == leagueName):
                print(league["country"])
                return league["league_id"]
            
        print("Couldnt find any league with: {}, {}".format(countryName, leagueName))



def getTeamID(teamName, leagueID):
    """Gets all teams in a whole league, then narrows down to single team and returns teamID if found """

    rec = urllib.request.Request("https://api-football-v1.p.rapidapi.com/v2/teams/league/" + str(leagueID))

    rec.add_header("X-RapidAPI-Host", "api-football-v1.p.rapidapi.com")
    rec.add_header("X-RapidAPI-Key", "1acHO5cH5QmshrLw9WFJXPxKPIgEp1uE4YzjsnGOydel9eubG9")

    with urllib.request.urlopen(rec) as response:
        #print("Status code from response: {}".format(response.getcode()))
        #print("Status code from response: {}".format(response.getheaders()))
        decodedTeams = response.read()
    
        teams = json.loads(decodedTeams, encoding = "utf-8")
        teams = teams["api"]["teams"]
        
    for team in teams:
        if (team["name"] == teamName):
            #print(team["team_id"])
            print(team)
            return team["team_id"]
    
    print("Team: {} not found....".format(teamName))


   
def getPastFixtures(countryName, leagueName, teamName):

    """
    Gets all fixtures for specified Team, then filters out all non-played results and returns the past matches
    Parameters: All strings
    Returns: A dictionary with all fixtures for the season for specified team in specified leauge. 
    """    

    leagueID = getLeagueID(countryName, leagueName)
    teamID = getTeamID(teamName, leagueID)
    #Constructing the right query
    endpointURL = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/{}/{}".format(teamID, leagueID)

    #Building up a Request object before sending it
    #It is an abstraction-class of a http request
    rec = urllib.request.Request(endpointURL)

    #Need to add this since i bought access on RapidAPI
    rec.add_header("X-RapidAPI-Host", "api-football-v1.p.rapidapi.com")
    #adding authentication key to access the API-Football API
    rec.add_header("X-RapidAPI-Key", "1acHO5cH5QmshrLw9WFJXPxKPIgEp1uE4YzjsnGOydel9eubG9")

    #make the request and pass in the Request object
    with urllib.request.urlopen(rec) as response:
        print("Status code from response: {}".format(response.getcode()))
        print("Status code from response: {}".format(response.getheaders()))
        decodedfixtures = response.read()
        
        fixtures = json.loads(decodedfixtures, encoding = "utf-8")
        fixtures = fixtures["api"]["fixtures"]
        
        #filter function with a lambda to filter out upcoming matches, eg: where half time score is None.
        #filter function keeps what evaluates to true and tosses the rest.
        fixtures = filter(lambda fixture: fixture["score"]["halftime"] is not None, fixtures)
        
        #for fixture in fixtures:
            #print("{} vs {}".format(fixture["homeTeam"]["team_name"], fixture["awayTeam"]["team_name"]))
            #print("score at halftime: {}".format(fixture["score"]["halftime"]))
            #print("\n")
        #print(fixtures)
    
    return fixtures

getPastFixtures("England", "Premier League", "Arsenal")



def getUpcomingFixturesForLeague(countryName, leagueName, howMany):
    """
    Should get upcoming fixtures for paramters:
    countryName : String
    leagueName : String
    howMany : Integer

    Returns: A 2D list with homeTeamName at 0 and awayTeamName at 1
    """
    upcomingFixtures = []

    leagueID = getLeagueID(countryName, leagueName)
    endpointURL = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{}/next/{}".format(leagueID, howMany)

    rec = urllib.request.Request(endpointURL)
    #Need to add this since i bought access on RapidAPI
    rec.add_header("X-RapidAPI-Host", "api-football-v1.p.rapidapi.com")
    #adding authentication key to access the API-Football API
    rec.add_header("X-RapidAPI-Key", "1acHO5cH5QmshrLw9WFJXPxKPIgEp1uE4YzjsnGOydel9eubG9")

    #make the request and pass in the Request object
    with urllib.request.urlopen(rec) as response:
        #print("Status code from response: {}".format(response.getcode()))
        #print("Status code from response: {}".format(response.getheaders()))
        decodedfixtures = response.read()
        
        fixtures = json.loads(decodedfixtures, encoding = "utf-8")

        nextFixtures = fixtures["api"]["fixtures"]

        for fixture in nextFixtures:
            print("{} vs {}".format(fixture["homeTeam"]["team_name"], fixture["awayTeam"]["team_name"]))
            upcomingFixtures.append([fixture["homeTeam"]["team_name"], fixture["awayTeam"]["team_name"]])

    return upcomingFixtures
