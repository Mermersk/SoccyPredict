import Fetcher as Fetch

#EDIT 27. Jan: Changed to fulltime instead of halftime
def calculateScoringChance(fixtures, homeORaway, teamName):
    
    """
    Arguments:
    fixtures : Dictionary - With past fixtures
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

    #goalScoredDecimalChance
    gsDecimalChance = round(wasGoalScored/totalMatces, 2)
    gcDecimalChance = round(wasGoalConceded/totalMatces, 2)
    #Calculating and printing out scoring stats
    print("Scored in {} matches out {} matches".format(wasGoalScored, totalMatces))
    print("Odds of {} scoring in a {} match: {} {}%"
    .format(teamName, homeORaway, gsDecimalChance, round((wasGoalScored/totalMatces) * 100)))

    #Calculating and printing out conceded stats
    print("Conceded in {} matches out of {} matches".format(wasGoalConceded, totalMatces))
    print("Odds of {} conceding in a {} match: {} {}%"
    .format(teamName, homeORaway, gcDecimalChance, round((wasGoalConceded/totalMatces) * 100)))

    print("\n")

    return gsDecimalChance, gcDecimalChance


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

    under05Percentage = under05 * 100
    over05Percentage = over05 * 100

    overDecimalBettingOdds = round(100 / over05Percentage, 3)
    underDecimalBettingOdds = round(100 / under05Percentage, 3)

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


def predictOne(countryName, leagueName, homeTeam, awayTeam):

    """
    Predicts The chance of homeTeam and awayTeam to score 1 goal in the first half.
    Arguments:
    countryName: String
    leagueName: String
    homeTeam: String
    awayTeam: String

    Returns: A betting label for this match with all relevant data and odds
    """
    homeTeamFixtures = Fetch.getPastFixtures(countryName, leagueName, homeTeam)
    awayTeamFixtures = Fetch.getPastFixtures(countryName, leagueName, awayTeam)

    homeScoring, homeConceding = calculateScoringChance(homeTeamFixtures, "home", homeTeam)
    awayScoring, awayConceding = calculateScoringChance(awayTeamFixtures, "away", awayTeam)

    #Home team odds of scoring in decimal
    homeDOddsOfScoring = (homeScoring + awayConceding) / 2.0
    awayDOddsOfScoring = (awayScoring + homeConceding) / 2.0

    #Home team Percentage odds of scoring at least 1 goal
    homePOddsOfScoring = homeDOddsOfScoring * 100
    awayPOddsOfScoring = awayDOddsOfScoring * 100

    awayPOddsOfCleanSheet = round(100 - homePOddsOfScoring)
    homePOddsOfCleanSheet = round(100 - awayPOddsOfScoring)

    #Perhaps later....
    #over05, under05 = WillThereBeGoal(homeDOddsOfScoring, awayDOddsOfScoring)

    bettingLabel = [leagueName, homeTeam, awayTeam, round(100/homePOddsOfScoring, 3), round(100/awayPOddsOfCleanSheet, 3), round(100/awayPOddsOfScoring, 3), round(100/homePOddsOfCleanSheet, 3)]

    print("{} to score against opponent is: {}% Betting odds: {} - Under 0.5: {}"
    .format(homeTeam, homePOddsOfScoring, round(100/homePOddsOfScoring, 3), round(100/awayPOddsOfCleanSheet, 3)))
    
    
    print("{} to score against opponent is: {}% Betting odds: {} - Under 0.5: {}"
    .format(awayTeam, awayPOddsOfScoring, round(100/awayPOddsOfScoring, 3), round(100/homePOddsOfCleanSheet, 3)))

    return bettingLabel