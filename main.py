import Fetcher as Fetch
import Predict as Predict
from tabulate import tabulate
import time

bettingLabelHeaders = ["League:", "HomeTeam:", "AwayTeam:", "H - Over 0.5:", "H - O 0.5 M", "HO Diff:", "H - Under 0.5:", "H - U 0.5 M", "HU Diff:", "A - Over 0.5:", "A - O 0.5 M", "AO Diff:", "A - Under 0.5:", "A - U 0.5 M", "AU Diff:"]#, "1H Over 0.5", "1H Under 0.5:", "H - Under 0.5 Pinny", "A - Under 0.5 Pinny", "H - Diff", "A - Diff"]

def printNewTableOrder(index, bettingLabels):
    bettingLabels.sort(key = lambda nestedList: nestedList[index])
    #Pretty print all games
    print(tabulate(bettingLabels, headers=bettingLabelHeaders, tablefmt="grid"))


def main():

    #Matches I want to check today, in the format:
    # countryName - String, leagueName - String, howmany - Integer
    todaysMatches = [
        
        #["South-Africa", "National First Division", 3],
        #["Switzerland", "Challenge League", 3],
        #["Spain", "Segunda B - Group 1", 9],
        #["Spain", "Segunda B - Group 2", 7],
        #["Spain", "Segunda B - Group 3", 7],
        #["Spain", "Segunda B - Group 4", 9],
        #["Israel", "Liga Leumit", 3],
        ["Italy", "Serie C", 1],
        ["France", "Ligue 2", 1],
        #["Switzerland", "Super League", 3],
        #["Northern-Ireland", "Championship", 5],
        #["Scotland", "League One", 5],
        
        ["Portugal", "Liga de Honra", 1],
        ["Portugal", "Primeira Liga", 2],
        #["Iran", "Persian Gulf Cup", 2], 
        #["Egypt", "Premier League", 1],
        
        #["Cyprus", "1. Division", 3],
        #["Germany", "Bundesliga 1", 4],
        ["Germany", "Liga 3", 1],
        #["Spain", "Primera Division", 4],
        #["Spain", "Segunda Division", 6],
        #["Egypt", "Premier League", 2],
        #["Belgium", "Jupiler Pro League", 1],
        ["Israel", "Ligat ha'Al", 1],
        #["South-Africa", "Premier Soccer League", 1],
        ["Netherlands", "Eerste Divisie", 2],
        #["Scotland", "Premiership", 2],
        #["Italy", "Serie A", 6],
        
        ["Italy", "Serie B", 1],

        ["Greece", "Super League", 2],
        #["India", "Indian Super League", 1],
        #["England", "Championship", 8],
        #["England", "League Two", 11],
        #["England", "National League", 12],
        #["Saudi-Arabia", "Pro League", 2],

        #["United-Arab-Emirates", "Arabian Gulf League", 3],

        ["Turkey", " Super Lig", 2],
        ["Turkey", "TFF 1. Lig", 1],
        
        #["Australia", "A-League", 1],
        
    ]


    bettingLabels = []
    
    for match in todaysMatches: 
        
        upcomingLeagueFixtures = Fetch.getUpcomingFixturesForLeague(match[0], match[1], match[2])

        for fixture in upcomingLeagueFixtures:
            bettingLabel = Predict.predictOne(match[0], match[1], fixture[0], fixture[1])
            marketOdds = Fetch.getScoringOdds(fixture[2])

            #print(type(marketOdds[0]))
            #print(type(bettingLabel[3]))
            bettingLabel.insert(4, marketOdds[0])
            bettingLabel.insert(5, float(marketOdds[0]) - bettingLabel[3])
            bettingLabel.insert(7, marketOdds[1])
            bettingLabel.insert(8, float(marketOdds[1]) - bettingLabel[6])
            bettingLabel.insert(10, marketOdds[2])
            bettingLabel.insert(11, float(marketOdds[2]) - bettingLabel[9])
            bettingLabel.insert(13, marketOdds[3])
            bettingLabel.insert(14, float(marketOdds[3]) - bettingLabel[12])
            #eventID, leagueID = Fetch.getLeagueAndEvent(fixture[0], fixture[1])
            #if eventID is not None:
                #underOdds = Fetch.getOdds(leagueID, eventID)
                #bettingLabel.append(underOdds[0])
                #bettingLabel.append(underOdds[1])
                #if underOdds[0] is not None:
                    #HUnder05Diff = underOdds[0] - bettingLabel[4]
                #else:
                    #HUnder05Diff = 0
                
                #if underOdds[1] is not None:
                    #AUnder05Diff = underOdds[1] - bettingLabel[6]
                #else:
                    #AUnder05Diff = 0
                

                #bettingLabel.append(HUnder05Diff)
                #bettingLabel.append(AUnder05Diff)
            #else:
                #bettingLabel.append(0)
                #bettingLabel.append(0)
                #bettingLabel.append(0)
                #bettingLabel.append(0)
                


            bettingLabels.append(bettingLabel)
            time.sleep(0.5)

    #Printing first results:
    print(tabulate(bettingLabels, headers=bettingLabelHeaders, tablefmt="grid"))
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
#eventID, leagueID = Fetch.getLeagueAndEvent("Real Madrid", "Atletico Madrid")
#if (eventID is not None):
    #print("EventID: {} leagueID: {}".format(eventID, leagueID))
    #Fetch.getOdds(leagueID, eventID)
