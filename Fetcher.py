import urllib.request
import json
import base64

#------------------------------- All functions below here make calls to api-football---------------

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
    """Finds the league ID of a league. By default it will return the current live league(2019)"""

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
    Returns: A list with all fixtures for the season for specified team in specified leauge. 
    """    
    #if (teamName == "Nuova Cosenza"):
        #teamName = "Cosenza"

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
        #Note 16 feb: wrap filter in list method, so I get back a list but not a "filter object"
        fixtures = list(filter(lambda fixture: fixture["score"]["fulltime"] is not None, fixtures))

        #fixtures = {k:v is not None for (k,v) in fixtures.items()}
        
        #for fixture in fixtures:
            #print("{} vs {}".format(fixture["homeTeam"]["team_name"], fixture["awayTeam"]["team_name"]))
            #print("score at halftime: {}".format(fixture["score"]["halftime"]))
            #print("\n")
        #print(fixtures)
    
    return fixtures

#getPastFixtures("England", "Premier League", "Arsenal")



def getUpcomingFixturesForLeague(countryName, leagueName, howMany):
    """
    Should get upcoming fixtures for paramters:
    countryName : String
    leagueName : String
    howMany : Integer

    Returns: A list with homeTeamName at 0, awayTeamName at 1 and fixture_id at 2
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
            upcomingFixtures.append([fixture["homeTeam"]["team_name"], fixture["awayTeam"]["team_name"], fixture["fixture_id"]])

    return upcomingFixtures



def getScoringOdds(fixtureID):

    """
    Arguments: FixtureID - Int
    Gets the home team and away team to score odds and BTTS yes/no odds from MarathonBet (via api-football).
    Returns: A list with 4 items [HOver05, HUnder05, AOver05, AUnder05]
             A list with 2 items [bttsYes, bttsNo]
    """
    print(type(fixtureID))
    #Marathonbet has ID of: 2
    
    endpointURL = "https://api-football-v1.p.rapidapi.com/v2/odds/fixture/{}/bookmaker/2/labels/43".format(fixtureID)

    rec = urllib.request.Request(endpointURL)
    #Need to add this since i bought access on RapidAPI
    rec.add_header("X-RapidAPI-Host", "api-football-v1.p.rapidapi.com")
    #adding authentication key to access the API-Football API
    rec.add_header("X-RapidAPI-Key", "1acHO5cH5QmshrLw9WFJXPxKPIgEp1uE4YzjsnGOydel9eubG9")

    #make the request and pass in the Request object
    with urllib.request.urlopen(rec) as response:
        #print("Status code from response: {}".format(response.getcode()))
        #print("Status code from response: {}".format(response.getheaders()))
        decodedResponse = response.read()
        
        dictResponse = json.loads(decodedResponse, encoding = "utf-8")
       
        try:
            dictResponse = dictResponse["api"]["odds"][0]["bookmakers"][0]["bets"]
        except IndexError:
            return [], []

        #odds values will be zero if they are not found at MarathonBet
        HOver05 = 0.0
        HUnder05 = 0.0
        AOver05 = 0.0
        AUnder05 = 0.0
        bttsYes = 0.0
        bttsNo = 0.0

        #labels in api-football: Home team to score a goal id: 43, away team to score a goal: 44
        for row in dictResponse:
            #print(row["label_name"])
            if row["label_id"] == 43:
                HOver05 = row["values"][0]["odd"]
                HUnder05 = row["values"][1]["odd"]

            if row["label_id"] == 44:
                AOver05 = row["values"][0]["odd"]
                AUnder05 = row["values"][1]["odd"]

            if row["label_name"] == "Both Teams Score":
                bttsYes = row["values"][0]["odd"]
                bttsNo = row["values"][1]["odd"]
      

    return [HOver05, HUnder05, AOver05, AUnder05], [bttsYes, bttsNo]



def getDCOdds(fixtureID):

    #LabelID for double chance is 12
    endpointURL = "https://api-football-v1.p.rapidapi.com/v2/odds/fixture/{}/bookmaker/2/labels/12".format(fixtureID)

    rec = urllib.request.Request(endpointURL)
    #Need to add this since i bought access on RapidAPI
    rec.add_header("X-RapidAPI-Host", "api-football-v1.p.rapidapi.com")
    #adding authentication key to access the API-Football API
    rec.add_header("X-RapidAPI-Key", "1acHO5cH5QmshrLw9WFJXPxKPIgEp1uE4YzjsnGOydel9eubG9")

    with urllib.request.urlopen(rec) as response:

        decodedResponse = response.read()
        #print(type(decodedResponse))

        dictResponse = json.loads(decodedResponse, encoding = "utf-8")

        try:
            dictResponse = dictResponse["api"]["odds"][0]["bookmakers"][0]["bets"]
        except IndexError:
            return 0.0, 0.0

        homeDC = 0.0
        awayDC = 0.0

        #print(type(dictResponse))
        #print(dictResponse)

        for row in dictResponse:
            if (row["label_name"] == "Double Chance"):
                print(row)
                try:
                    homeDC = row["values"][0]["odd"]
                    awayDC = row["values"][2]["odd"]
                except IndexError:
                    return 0.0, 0.0


    return homeDC, awayDC






#------------------------------- All functions below here make calls to Pinnacle---------------
#Edit: Jan 27: Pinnacle functions not currently in use, since Pinny offer odds often only a few
#hours before matvh, and team names differ from api-football API where stats are gotten from.


def getLeagueAndEvent(homeTeam, awayTeam):
    """
    Should get the Pinncale LeagueId and EventID for certain match
    """

    endpointURL = "https://api.pinnacle.com/v1/fixtures?sportId=29"

    rec = urllib.request.Request(endpointURL)

    #encodes to a base64 Bytes object
    pinncaleCredentials = base64.b64encode(b"IS925238:Maximus_1")
    #Decodes the Bytes object to string, whic is: SVM5MjUyMzg6TWF4aW11c18x
    pinncaleCredentials = pinncaleCredentials.decode()
    
    #authValue = "Basic " + pinncaleCredentials
    rec.add_header("Authorization", "Basic {}".format(pinncaleCredentials))
    rec.add_header("Accept", "application/json")

    with urllib.request.urlopen(rec) as response:

        #print("Status code from response: {}".format(response.getcode()))
        #print("Status code from response: {}".format(response.getheaders()))
        decodedResponse = response.read()
        
        dictResponse = json.loads(decodedResponse, encoding = "utf-8")

        #print(dictResponse)

        for fixture in dictResponse["league"]:
            for match in fixture["events"]:
                if homeTeam in match["home"] and awayTeam in match["away"]:
                    print("Found match: {}".format(match))
                    EventID = match["id"]
                    LeagueID = fixture["id"]
                    return EventID, LeagueID
                
        return None, None
        #print(type(dictResponse))
        #print(dictResponse)

def getOdds(leagueID, eventID):

    """
    Currently gets the under 0.5 goals for both hometeam and awayteam.
    Returns: An list iwht 2 items, first is hometeam and second item in awayteam
    """

    underOdds = []

    for i in range(1, 3):

        endpointURL = "https://api.pinnacle.com/v1/line?sportId=29&handicap=0.5&oddsFormat=Decimal&periodNumber=1&betType=TEAM_TOTAL_POINTS&team=Team{}&side=UNDER&leagueId={}&eventId={}".format(i, leagueID, eventID)
        #endpointURL = "https://api.pinnacle.com/v1/odds?sportId=29&oddsFormat=Decimal&eventIds=" + str(eventID)
        rec = urllib.request.Request(endpointURL)

        #encodes to a base64 Bytes object
        pinncaleCredentials = base64.b64encode(b"IS925238:Maximus_1")
        #Decodes the Bytes object to string, whic is: SVM5MjUyMzg6TWF4aW11c18x
        pinncaleCredentials = pinncaleCredentials.decode()
        
        #authValue = "Basic " + pinncaleCredentials
        rec.add_header("Authorization", "Basic {}".format(pinncaleCredentials))
        rec.add_header("Accept", "application/json")

        with urllib.request.urlopen(rec) as response:

            #print("Status code from response: {}".format(response.getcode()))
            #print("Status code from response: {}".format(response.getheaders()))
            decodedResponse = response.read()
            
            dictResponse = json.loads(decodedResponse, encoding = "utf-8")
            #print(dictResponse)
            if dictResponse["status"] == "SUCCESS":
                under05Price = dictResponse["price"]
                underOdds.append(under05Price)
            else:
                under05Price = None
                underOdds.append(under05Price)
            
    
    print("Home U 0.5: {}  :  Away U 0.5: {}".format(underOdds[0], underOdds[1]))

    return underOdds