import Fetcher as Fetch
import Predict as Predict
from tabulate import tabulate
import time

bettingLabelHeaders = ["League:", "HomeTeam:", "AwayTeam:", "H - Over 0.5:", "H - Under 0.5:", "A - Over 0.5:", "A - Under 0.5:", "1H Over 0.5", "1H Under 0.5:"]

def printNewTableOrder(index, bettingLabels):
    bettingLabels.sort(key = lambda nestedList: nestedList[index])
    #Pretty print all games
    print(tabulate(bettingLabels, headers=bettingLabelHeaders))


def main():

    #Matches I want to check today, in the format:
    # countryName - String, leagueName - String, howmany - Integer
    todaysMatches = [
        ["England", "Premier League", 3],
        ["England", "Championship", 2],
        ["Scotland", "Premiership", 6],
        ["Greece", "Super League", 5],
        ["India", "Indian Super League", 1],

        
        ["Italy", "Serie C", 15],
        
    ]

    #["South-Africa", "National First Division", 2],

    bettingLabels = []
    
    for match in todaysMatches: 
        upcomingLeagueFixtures = Fetch.getUpcomingFixturesForLeague(match[0], match[1], match[2])

        for fixture in upcomingLeagueFixtures:
            bettingLabel = Predict.predictOne(match[0], match[1], fixture[0], fixture[1])
            bettingLabels.append(bettingLabel)
            time.sleep(11)

    #Printing first results:
    print(tabulate(bettingLabels, headers=bettingLabelHeaders))
    #Terminal application loop - Mainly for sorting data in columns in different ways:
    stop = False
    while stop is not True:
        i = input("Insert index-number to be sorted on or q to quit: ")
        if i == "q":
            stop = True
            break
        index = int(i)
        printNewTableOrder(index, bettingLabels)


main()


