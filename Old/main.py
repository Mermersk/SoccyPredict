import csv

print("hello")
mainData = []

with open("I1.csv") as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        mainData.append(row)
    
#print(len(mainData))

def getHomeMatches(teamName):
    onlyHomeMatches = []
    for row in mainData:
        if row[3] == teamName:
            #print(row)
            onlyHomeMatches.append(row)

    return onlyHomeMatches

def getAwayMatches(teamName):
    onlyAwayMatches = []
    for row in mainData:
        if row[4] == teamName:
            #print(row)
            onlyAwayMatches.append(row)

    return onlyAwayMatches
#getAwayMatches("Betis")

#See notes.txt on football-data.co.uk for the possible column names
def getColumnIndex(columnName):
    for i in range(len(mainData[0])):
        if (mainData[0][i] == columnName):
            return i

#Gets halftime goals scored/conceded and calculates some odds on that
def getHalftimeGoals(teamName, homeORaway):
    if (homeORaway == "home"):
        matches = getHomeMatches(teamName)
        opponent = getColumnIndex("AwayTeam")
    else:
        matches = getAwayMatches(teamName)
        opponent = getColumnIndex("HomeTeam")

    columnNames = ["HTHG", "HTAG"]
    columnIndices = [getColumnIndex(columnNames[0]), getColumnIndex(columnNames[1])]

    totalMatces = 0
    # 1 means yes and 0 means no
    wasGoalScored = 0
    wasGoalConceded = 0

    for row in matches:
        if (homeORaway == "home"):
            #print("{} vs {}".format(teamName, row[opponent]))
            targetTeam = 0
            oppo = 1
        else:
            #print("{} vs {}".format(row[opponent], teamName))
            targetTeam = 1
            oppo = 0

        #print("Team goals scored({} {}):".format(teamName, homeORaway))
        #print(row[columnIndices[targetTeam]])

        #print("Team conceded({} {}):".format(teamName, homeORaway))
        #print(row[columnIndices[oppo]])

        totalMatces += 1
        if (int(row[columnIndices[targetTeam]]) > 0):
            wasGoalScored += 1

        if (int(row[columnIndices[oppo]]) > 0):
            wasGoalConceded += 1

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
#[
# Predicts wether a goal for each team will be scored in
# the first half.
# ]
def predict(homeTeam, awayTeam):
    homeScoring, homeConceding = getHalftimeGoals(homeTeam, "home")
    awayScoring, awayConceding = getHalftimeGoals(awayTeam, "away")

    #Home team Percentage odds of scoring at least 1 goal
    homePOddsOfScoring = round(((homeScoring + awayConceding) / 2.0) * 100)
    awayPOddsOfScoring = round(((awayScoring + homeConceding) / 2.0) * 100)

    print("{} to score against opponent is: {}% Betting odds: {}"
    .format(homeTeam, homePOddsOfScoring, round(100/homePOddsOfScoring, 3)))
    
    print("{} to score against opponent is: {}% Betting odds: {}"
    .format(awayTeam, awayPOddsOfScoring, round(100/awayPOddsOfScoring, 3)))

predict("Milan", "Sampdoria")

