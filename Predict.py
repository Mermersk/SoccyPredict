import Fetcher as Fetch
import Utils

#EDIT 27. Jan: Changed to fulltime instead of halftime
def calculateScoringChance(fixtures, homeORaway, teamName):
    
    """
    Arguments:
    fixtures : List (containing other lists and dicts) - With past fixtures
    homeORaway: String - Wether we are looking at home or away form of team
    teamName: String - Name of team we are calculalating scoring/conceding chance

    Returns: gsDecimalChance and gcDecimalChance. (goalScoredchance and goalConcededChance)
    The chances of goal being scored or conceded by X team in a decimal range (0.0 to 1.0)
    """

    totalMatces = 0
    # 1 means yes and 0 means no
    wasGoalScored = 0
    wasGoalConceded = 0

    for fixture in fixtures:
        
        if (homeORaway == "home"):
            if (teamName == fixture["homeTeam"]["team_name"]):
                print("{} vs {}".format(fixture["homeTeam"]["team_name"], fixture["awayTeam"]["team_name"]))
                #print("score at halftime: {}".format(fixture["score"]["halftime"]))
                print("score at fulltime: {}".format(fixture["score"]["fulltime"]))

                fullTimeScore = fixture["score"]["fulltime"]
                totalMatces += 1
                if (int(fullTimeScore[0]) > 0):
                    wasGoalScored += 1

                if (int(fullTimeScore[2]) > 0):
                    wasGoalConceded += 1

        elif (homeORaway == "away"):
            if (teamName == fixture["awayTeam"]["team_name"]):
                print("{} vs {}".format(fixture["homeTeam"]["team_name"], fixture["awayTeam"]["team_name"]))
                #print("score at halftime: {}".format(fixture["score"]["halftime"]))
                print("score at fulltime: {}".format(fixture["score"]["fulltime"]))
                    
                fullTimeScore = fixture["score"]["fulltime"]
                totalMatces += 1

                if (int(fullTimeScore[0]) > 0):
                    wasGoalConceded += 1

                if (int(fullTimeScore[2]) > 0):
                    wasGoalScored += 1


    #print("Total {} matches of {}: {}".format(homeORaway, teamName, totalMatces))
    #print("{} {} scored in {} matches out of total {}"
    #.format(teamName, homeORaway, str(wasGoalScored), str(totalMatces)))
    #print("{} {} conceded in {} matches out of total {}"
    #.format(teamName, homeORaway, str(wasGoalConceded), str(totalMatces)))

    #Avoid division by zero error. Anyway if totalMatches is zero, then no analysis can be made.
    if totalMatces == 0:
        return 0, 0
    
    gsDecimalChance = round(wasGoalScored/totalMatces, 2)
    gcDecimalChance = round(wasGoalConceded/totalMatces, 2)
    #Calculating and printing out scoring stats
    print("Scored in {} matches out {} matches".format(wasGoalScored, totalMatces))
    print("Odds of {} scoring in a {} match: {} {}%"
    .format(teamName, homeORaway, gsDecimalChance, round(Utils.fromDecimalProbToPercentage(gsDecimalChance))))

    #Calculating and printing out conceded stats
    print("Conceded in {} matches out of {} matches".format(wasGoalConceded, totalMatces))
    print("Odds of {} conceding in a {} match: {} {}%"
    .format(teamName, homeORaway, gcDecimalChance, round(Utils.fromDecimalProbToPercentage(gcDecimalChance))))

    print("\n")

    return gsDecimalChance, gcDecimalChance


def calculateWinDrawChance(fixtures, homeORaway, teamName):

    totalMatches = 0
    winDrawScore = 0

    winPoints = 1.0
    drawPoints = 0.8

    maxPoints = 0

    for fixture in fixtures:

        if (homeORaway == "home"):
            if (teamName == fixture["homeTeam"]["team_name"]):

                fullTimeScore = fixture["score"]["fulltime"]
                homeTeamScore = int(fullTimeScore[0])
                awayTeamScore = int(fullTimeScore[2])

                maxPoints += winPoints
                totalMatches += 1

                outcome = determineOutcome(homeTeamScore, awayTeamScore)

                if (outcome == "homeWin"):
                    winDrawScore += winPoints

                if (outcome == "draw"):
                    winDrawScore += drawPoints

        elif (homeORaway == "away"):
            if (teamName == fixture["awayTeam"]["team_name"]):

                fullTimeScore = fixture["score"]["fulltime"]
                homeTeamScore = int(fullTimeScore[0])
                awayTeamScore = int(fullTimeScore[2])

                maxPoints += winPoints
                totalMatches += 1

                outcome = determineOutcome(homeTeamScore, awayTeamScore)

                if (outcome == "awayWin"):
                    winDrawScore += winPoints

                if (outcome == "draw"):
                    winDrawScore += drawPoints


    #maxPointsDecimalProb = maxPoints/totalMatches

    winDrawScoreDecimalProb = round(winDrawScore/totalMatches, 3)

    print("{} Has a: {} chance of DC".format(teamName, winDrawScoreDecimalProb))

    return winDrawScoreDecimalProb



def determineOutcome(homeTeamScore, awayTeamScore):
    if (homeTeamScore > awayTeamScore):
        return "homeWin"

    if (homeTeamScore < awayTeamScore):
        return "awayWin"

    return "draw"


"""
Claculates odds on over and under 0.5 goals in first half.

Parameters: home and way team scoring chance in decimal range (0.0 to 1.0)
Returns: Decimal porbability of the over/under 0.5 goals in first half
"""
def WillThereBeGoal(homeTeamSD, awayTeamSD):

    """
    #Getting average of 2 percentages. (Add them together and divide by number of percentages)
    totalScoringCapacity = round((homeTeamSP + awayTeamSP) / 2.0)
    #over is odds of it being over 0.5 goals
    over = totalScoringCapacity
    under = 100 - over

    overDecimalBettingOdds = round(100 / over, 3)
    underDecimalBettingOdds = round(100 / under, 3)

    print("Over 0.5: {} - Under 0.5: {}".format(overDecimalBettingOdds, underDecimalBettingOdds))

    """

    """
    # The chance of 2 independent events both occuring is(Multiplication rule 1): P(A and B) = P(A) * P(B)
    # If team A and team B have 50% (0.5) chance of scoring each, then the chance of both scoring is: 0.5 * 0.5 = 0.25 (25%)
    # Chanche of 1 team scoring: P(A) + P(B) - P(A and B)
    # Chance of both events not happening is: (1.0 - P(A)) * (1.0 - P(B)) = P(Not A and Not B)
    """

    under05 = ((1.0 - homeTeamSD) * (1.0 - awayTeamSD))
    #over is odds of it being over 0.5 goals
    over05 = 1.0 - under05

    under05Percentage = Utils.fromDecimalProbToPercentage(under05)
    over05Percentage = Utils.fromDecimalProbToPercentage(over05)

    overDecimalBettingOdds = round(Utils.fromPercentageToOdds(over05Percentage), 3)
    underDecimalBettingOdds = round(Utils.fromPercentageToOdds(under05Percentage), 3)

    print("Over 0.5: {} - Under 0.5: {}".format(overDecimalBettingOdds, underDecimalBettingOdds))

    return overDecimalBettingOdds, underDecimalBettingOdds

    """
    #Over-under- different calculation under here:

    bothTeamsS = ((homeScoring + awayScoring) / 2.0) * 100
    bothTeamsC = ((homeConceding + awayConceding) / 2.0) * 100

    chanceOfGoal = (bothTeamsS + bothTeamsC) / 2.0

    over2 = chanceOfGoal
    under2 = 100 - chanceOfGoal

    over2DecimalBettingOdds = round(100 / over2, 3)
    under2DecimalBettingOdds = round(100 / under2, 3)

    print("V2 Over 0.5: {} - Under 0.5: {}".format(over2DecimalBettingOdds, under2DecimalBettingOdds))
    """

def drawPredict(homeTeamSD, awayTeamSD):

    lowGoalTally = ((1.0 - homeTeamSD) * (1.0 - awayTeamSD))
    #over is odds of it being over 0.5 goals
    highGoalTally = 1.0 - lowGoalTally

    lowGoalTallyPercentage = Utils.fromDecimalProbToPercentage(lowGoalTally)
    highGoalTallyPercentage = Utils.fromDecimalProbToPercentage(highGoalTally)

    #So that I dont get ZeroDivisonError, This will happen when the chance is 0% 
    #If so then I multiply by 0.1 thiss will return odds of 1000 (almost impossible)
    if (lowGoalTallyPercentage == 0.0):
        lowGoalDecimalBettingOdds = 0.1
    else:
        lowGoalDecimalBettingOdds = round(Utils.fromPercentageToOdds(lowGoalTallyPercentage), 3)


    highGoalDecimalBettingOdds = round(Utils.fromPercentageToOdds(highGoalTallyPercentage), 3)
    
    #print("Over 0.5: {} - Under 0.5: {}".format(highGoalDecimalBettingOdds, lowGoalDecimalBettingOdds))

    return highGoalDecimalBettingOdds, lowGoalDecimalBettingOdds


def bttsPredict(homeTeamSD, awayTeamSD):
    """
    Calculates the chance of BTTS
    """
    bttsYes = homeTeamSD * awayTeamSD
    bttsNo = 1.0 - bttsYes

    bttsYesOdds = round(Utils.fromDecimalProbToOdds(bttsYes), 3)
    bttsNoOdds = round(Utils.fromDecimalProbToOdds(bttsNo), 3)

    return bttsYesOdds, bttsNoOdds

def predictOne(countryName, leagueName, homeTeam, awayTeam):

    """
    Predicts The chance of homeTeam and awayTeam to score 1 goal in the first half.
    Arguments:
    countryName: String
    leagueName: String
    homeTeam: String
    awayTeam: String

    Returns: list labels,  other lists of bettinglabels.
    """
    #Represent all labels, will contain other lists(f.ex bettingLabelDraw)
    labels = []

    homeTeamFixtures = Fetch.getPastFixtures(countryName, leagueName, homeTeam)
    awayTeamFixtures = Fetch.getPastFixtures(countryName, leagueName, awayTeam)

    homeDCChance = calculateWinDrawChance(homeTeamFixtures, "home", homeTeam)
    awayDCChance = calculateWinDrawChance(awayTeamFixtures, "away", awayTeam) 

    #print(homeTeamFixtures)

    homeScoring, homeConceding = calculateScoringChance(homeTeamFixtures, "home", homeTeam)
    awayScoring, awayConceding = calculateScoringChance(awayTeamFixtures, "away", awayTeam)

    #print(homeTeamFixtures)
    #print("homescoring: {}".format(homeScoring))

    #Home team odds of scoring in decimal
    homeDOddsOfScoring = (homeScoring + awayConceding) / 2.0
    awayDOddsOfScoring = (awayScoring + homeConceding) / 2.0

    #Home team Percentage odds of scoring at least 1 goal
    homePOddsOfScoring = Utils.fromDecimalProbToPercentage(homeDOddsOfScoring)
    awayPOddsOfScoring = Utils.fromDecimalProbToPercentage(awayDOddsOfScoring)
    awayPOddsOfCleanSheet = round(100 - homePOddsOfScoring)
    homePOddsOfCleanSheet = round(100 - awayPOddsOfScoring)

    #These 2 if statements are simply to prevent ZeroDivisionError (Very rare that these 2 variables are 0)
    if (awayPOddsOfCleanSheet == 0):
        awayPOddsOfCleanSheet = 1
    if (homePOddsOfCleanSheet == 0):
        homePOddsOfCleanSheet = 1

    #Converting to european betting odds
    homeBettingOddsOfScoring = round(Utils.fromPercentageToOdds(homePOddsOfScoring), 3)
    awayBettingOddsOfScoring = round(Utils.fromPercentageToOdds(awayPOddsOfScoring), 3)
    homeBettingOddsOfCleanSheet = round(Utils.fromPercentageToOdds(homePOddsOfCleanSheet), 3)
    awayBettingOddsOfCleanSheet = round(Utils.fromPercentageToOdds(awayPOddsOfCleanSheet), 3)
 
    noDraw, yesDraw = drawPredict(homeDOddsOfScoring, awayDOddsOfScoring)

    bettingLabelDraw = [leagueName, homeTeam, awayTeam, homePOddsOfScoring, awayPOddsOfScoring, noDraw, yesDraw, homePOddsOfScoring - awayPOddsOfScoring]

    bttsYes, bttsNo = bttsPredict(homeDOddsOfScoring, awayDOddsOfScoring)

    bettingLabelBTTS = [leagueName, homeTeam, awayTeam, bttsYes, bttsNo]

    bettingLabelDC = [leagueName, homeTeam, awayTeam, homeDCChance, awayDCChance]   

    #Change 3. feb: Taking out all under-bets, only want over0.5, betting label too big...
    bettingLabel = [leagueName, homeTeam, awayTeam, homeBettingOddsOfScoring, awayBettingOddsOfScoring]

    print("{} to score against opponent is: {}% Betting odds: {} - Under 0.5: {}"
    .format(homeTeam, homePOddsOfScoring, homeBettingOddsOfScoring, awayBettingOddsOfCleanSheet))
    
    print("{} to score against opponent is: {}% Betting odds: {} - Under 0.5: {}"
    .format(awayTeam, awayPOddsOfScoring, awayBettingOddsOfScoring, homeBettingOddsOfCleanSheet))

    labels.append(bettingLabel)
    labels.append(bettingLabelBTTS)
    labels.append(bettingLabelDraw)
    labels.append(bettingLabelDC)

    return labels