import urllib.request
import json

def saveAsJSON(dictionary):
    with open("leagues.json", "w") as leagueFile:
        json.dump(dictionary, leagueFile)

#Finds the league ID of a league. By defualt it will return the current live league(2019)
def getLeagueID(countryName, leagueName):
    with open("leagues.json", "r") as leagueFile:
        leagues = json.load(leagueFile)["api"]["leagues"]
        for league in leagues:
            if (league["country"] == countryName and league["season"] == 2019 and league["name"] == leagueName):
                print(league["country"])
                return league["league_id"]
            
        print("Couldnt find any league with: {}, {}".format(countryName, leagueName))

#getLeagueID("Egypt", "Premier League")

#Gets all teams in a whole league, then narrows down to single team and returns teamID if found
def getTeamID(teamName, leagueID):
    
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
    
    print("Team not found....")

#getTeamID("Ismaily SC", "972")

"""
Parameters: All strings
returns: A dictionary with all fixtures for the season for specified team in specified leauge. 
"""
def getFixtures(countryName, leagueName, teamName):
    #get fixtures based on .../fixture/team/teamID/leagueID
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
        #saveAsJSON(fixtures)
     
        #print(len(fixtures))
        #for fixture in fixtures["api"]["fixtures"]:
            #print("{} vs {}".format(fixture["homeTeam"]["team_name"], fixture["awayTeam"]["team_name"]))
            #print("score at halftime: {}".format(fixture["score"]["halftime"]))
            #print("\n")
        #print(fixtures)
    
    return fixtures["api"]["fixtures"]

"""
Parameter: a dictionary with fixtures

Returns: gsDecimalChance and gcDecimalChance. (goalScoredchanche and goalConcededChance)
The chances of goal being scored or conceded by X team in a decimal range (0.0 to 1.0)
"""
def calculateHTChance(fixtures, homeORaway, teamName):
    
    totalMatces = 0
    # 1 means yes and 0 means no
    wasGoalScored = 0
    wasGoalConceded = 0
    #Could be either away or home matches
    matches = {}

    for fixture in fixtures:
        if fixture["score"]["halftime"] is not None:
            if (homeORaway == "home"):
                if (teamName == fixture["homeTeam"]["team_name"]):
                    print("{} vs {}".format(fixture["homeTeam"]["team_name"], fixture["awayTeam"]["team_name"]))
                    print("score at halftime: {}".format(fixture["score"]["halftime"]))

                    halfTimeScore = fixture["score"]["halftime"]
                    totalMatces += 1
                    if (int(halfTimeScore[0]) > 0):
                        wasGoalScored += 1

                    if (int(halfTimeScore[2]) > 0):
                        wasGoalConceded += 1

            elif (homeORaway == "away"):
                if (teamName == fixture["awayTeam"]["team_name"]):
                    print("{} vs {}".format(fixture["homeTeam"]["team_name"], fixture["awayTeam"]["team_name"]))
                    print("score at halftime: {}".format(fixture["score"]["halftime"]))
                    
                    halfTimeScore = fixture["score"]["halftime"]
                    totalMatces += 1

                    if (int(halfTimeScore[0]) > 0):
                        wasGoalConceded += 1

                    if (int(halfTimeScore[2]) > 0):
                        wasGoalScored += 1


    #print("Total {} matches of {}: {}".format(homeORaway, teamName, totalMatces))
    #print("{} {} scored in {} matches out of total {}"
    #.format(teamName, homeORaway, str(wasGoalScored), str(totalMatces)))
    #print("{} {} conceded in {} matches out of total {}"
    #.format(teamName, homeORaway, str(wasGoalConceded), str(totalMatces)))

    #goalScoredDecimalChance
    gsDecimalChance = round(wasGoalScored/totalMatces, 2)
    gcDecimalChance = round(wasGoalConceded/totalMatces, 2)
    #Calculating and printing out scoring stats
    print("Scored in {} matches out {} matches".format(wasGoalScored, totalMatces))
    print("Odds of {} scoring in a {} match in first half is: {} {}%"
    .format(teamName, homeORaway, gsDecimalChance, round((wasGoalScored/totalMatces) * 100)))

    #Calculating and printing out conceded stats
    print("Conceded in {} matches out of {} matches".format(wasGoalConceded, totalMatces))
    print("Odds of {} conceding in a {} match in first half is: {} {}%"
    .format(teamName, homeORaway, gcDecimalChance, round((wasGoalConceded/totalMatces) * 100)))

    print("\n")

    return gsDecimalChance, gcDecimalChance


def printAllTeamsInLeague(countryName, leagueName):

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


"""
Claculates odds on over and under 0.5 goals in first half.

Parameters: home and way team scoring chance in percentage rnge (0-100%)
Returns: Decimal betting odds of the over/under 0.5 goals in first half
"""
def WillThereBeGoal(homeTeamSP, awayTeamSP, homeScoring, homeConceding, awayScoring, awayConceding):

    #Getting average of 2 percentages. (Add them together and divide by number of percentages)
    totalScoringCapacity = round((homeTeamSP + awayTeamSP) / 2.0)
    #over is odds of it being over 0.5 goals
    over = totalScoringCapacity
    under = 100 - over

    overDecimalBettingOdds = round(100 / over, 3)
    underDecimalBettingOdds = round(100 / under, 3)

    print("Over 0.5: {} - Under 0.5: {}".format(overDecimalBettingOdds, underDecimalBettingOdds))

    #Over-under- different calculation under here:

    bothTeamsS = ((homeScoring + awayScoring) / 2.0) * 100
    bothTeamsC = ((homeConceding + awayConceding) / 2.0) * 100

    chanceOfGoal = (bothTeamsS + bothTeamsC) / 2.0

    over2 = chanceOfGoal
    under2 = 100 - chanceOfGoal

    over2DecimalBettingOdds = round(100 / over2, 3)
    under2DecimalBettingOdds = round(100 / under2, 3)

    print("V2 Over 0.5: {} - Under 0.5: {}".format(over2DecimalBettingOdds, under2DecimalBettingOdds))


#[
# Predicts wether a goal for each team will be scored in
# the first half.
# ]
def predict(countryName, leagueName, homeTeam, awayTeam):

    homeTeamFixtures = getFixtures(countryName, leagueName, homeTeam)
    awayTeamFixtures = getFixtures(countryName, leagueName, awayTeam)

    homeScoring, homeConceding = calculateHTChance(homeTeamFixtures, "home", homeTeam)
    awayScoring, awayConceding = calculateHTChance(awayTeamFixtures, "away", awayTeam)

    #Home team Percentage odds of scoring at least 1 goal
    homePOddsOfScoring = round(((homeScoring + awayConceding) / 2.0) * 100)
    awayPOddsOfScoring = round(((awayScoring + homeConceding) / 2.0) * 100)

    print("{} to score against opponent is: {}% Betting odds: {}"
    .format(homeTeam, homePOddsOfScoring, round(100/homePOddsOfScoring, 3)))
    
    print("{} to score against opponent is: {}% Betting odds: {}"
    .format(awayTeam, awayPOddsOfScoring, round(100/awayPOddsOfScoring, 3)))

    WillThereBeGoal(homePOddsOfScoring, awayPOddsOfScoring, homeScoring, homeConceding, awayScoring, awayConceding)

#printAllTeamsInLeague("India", "Indian Super League")
predict("India", "Indian Super League", "Chennaiyin", "NorthEast United")