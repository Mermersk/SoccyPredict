import Fetcher as Fetch
import Predict as Predict
from tabulate import tabulate
import time

bettingLabelHeaders = ["League:", "HomeTeam:", "AwayTeam:", "H - Over 0.5:", "H - O 0.5 M", "HO Diff:", "H - Under 0.5:", "H - U 0.5 M", "HU Diff:", "A - Over 0.5:", "A - O 0.5 M", "AO Diff:", "A - Under 0.5:", "A - U 0.5 M", "AU Diff:"]#, "1H Over 0.5", "1H Under 0.5:", "H - Under 0.5 Pinny", "A - Under 0.5 Pinny", "H - Diff", "A - Diff"]
bettingLabelBTTSHeaders = ["League:", "HomeTeam:", "AwayTeam:", "BTTS Yes:", "BTTS Yes M:", "BTTS Yes Diff:", "BTTS No:", "BTTS No M:", "BTTS No Diff:"]
bettingLabelDrawHeaders = ["League:", "HomeTeam:", "AwayTeam:", "H Scoring Chance", "A Scoring Chance", "Draw No", "Draw Yes", "Diff Scoring capacity"]

def printNewTableOrder(index, bettingLabels, bettingLabelsBTTS, bettingLabelsDraw):
    try:
        bettingLabels.sort(key = lambda nestedList: nestedList[index])
    except TypeError:
        pass
    
    if (index < len(bettingLabelsBTTS[0])):
        bettingLabelsBTTS.sort(key = lambda nestedList: nestedList[index])

    if (index < len(bettingLabelsDraw[0])):
        bettingLabelsDraw.sort(key = lambda nestedList: nestedList[index])
    
    print(tabulate(bettingLabels, headers=bettingLabelHeaders, tablefmt="grid"))
    print(tabulate(bettingLabelsBTTS, headers=bettingLabelBTTSHeaders, tablefmt="grid"))
    print(tabulate(bettingLabelsDraw, headers=bettingLabelDrawHeaders, tablefmt="grid"))


def main():

    #Matches I want to check today, in the format:
    # countryName - String, leagueName - String, howmany - Integer
    todaysMatches = [
        ["Algeria", "Ligue 1", 4],
        ["Hungary", "NB I", 6],
        ["United-Arab-Emirates", "Arabian Gulf League", 3],
        ["Iran", "Persian Gulf Cup", 3],
        ["South-Africa", "Premier Soccer League", 3],
        ["Qatar", "Stars League", 2],
        ["Saudi-Arabia", "Pro League", 3],
        #["Switzerland", "Challenge League", 3],
        #["Spain", "Segunda B - Group 1", 9],
        #["Spain", "Segunda B - Group 2", 7],
        #["Spain", "Segunda B - Group 3", 7],
        #["Spain", "Segunda B - Group 4", 9],
        #["Israel", "Liga Leumit", 3],
        ["Italy", "Serie C", 3],
        ["France", "Ligue 2", 1],
        ["France", "Ligue 1", 6],
        #["France", "National", 8],
        #["Switzerland", "Super League", 3],
        ["Northern-Ireland", "Championship", 2],
        ["Scotland", "League One", 5],
        ["Scotland", "League Two", 5],
        
        ["Portugal", "Liga de Honra", 3],
        ["Portugal", "Primeira Liga", 3],
         
        #["Egypt", "Premier League", 2],
        
        ["Cyprus", "1. Division", 3],
        ["Germany", "Bundesliga 2", 3],
        ["Germany", "Bundesliga 1", 6],
        ["Germany", "Liga 3", 6],
        ["Spain", "Primera Division", 4],
        ["Spain", "Segunda Division", 4],
        #["Egypt", "Premier League", 2],
        ["Belgium", "Jupiler Pro League", 4],
        ["Israel", "Ligat ha'Al", 4],
        
        #["Netherlands", "Eerste Divisie", 8],
        ["Netherlands", "Eredivisie", 4],
        ["Scotland", "Championship", 4],
        ["Scotland", "Premiership", 5],
        ["Italy", "Serie A", 3],
        
        ["Italy", "Serie B", 5],

        ["Greece", "Super League", 3],
        ["India", "Indian Super League", 1],
        ["England", "Championship", 10],
        ["England", "League One", 11],
        ["England", "League Two", 12],
        ["England", "National League", 12],
        ["England", "Premier League", 8],
        

        
        #["Oman", "Professional League", 2],

        ["Turkey", " Super Lig", 3],
        ["Turkey", "TFF 1. Lig", 3],
        
        ["Australia", "A-League", 3],

    ]


    bettingLabels = []
    bettingLabelsBTTS = []
    bettingLabelsDraw = []
    
    for match in todaysMatches: 
        
        upcomingLeagueFixtures = Fetch.getUpcomingFixturesForLeague(match[0], match[1], match[2])

        for fixture in upcomingLeagueFixtures:
            allLabels = Predict.predictOne(match[0], match[1], fixture[0], fixture[1])
            bettingLabel = allLabels[0]
            bettingLabelBTTS = allLabels[1]
            bettingLabelDraw = allLabels[2]

            marketOdds, marketOddsBTTS = Fetch.getScoringOdds(fixture[2])

            #if not marketOdds, will detect if list is empty!
            if not marketOdds:
                continue
            #If any of odds were not available, then None type will be assigned to that item in the list, if this is the case we continue
           
            bettingLabel.insert(4, marketOdds[0])
            bettingLabel.insert(5, float(marketOdds[0]) - bettingLabel[3])
            bettingLabel.insert(7, marketOdds[1])
            bettingLabel.insert(8, float(marketOdds[1]) - bettingLabel[6])
            bettingLabel.insert(10, marketOdds[2])
            bettingLabel.insert(11, float(marketOdds[2]) - bettingLabel[9])
            bettingLabel.insert(13, marketOdds[3])
            bettingLabel.insert(14, float(marketOdds[3]) - bettingLabel[12])

            bettingLabelBTTS.insert(4, marketOddsBTTS[0])
            
            bettingLabelBTTS.insert(5, float(marketOddsBTTS[0]) - bettingLabelBTTS[3])
            bettingLabelBTTS.insert(7, marketOddsBTTS[1])
            bettingLabelBTTS.insert(8, float(marketOddsBTTS[1]) - bettingLabelBTTS[6])

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
                

            bettingLabelsBTTS.append(bettingLabelBTTS)
            bettingLabels.append(bettingLabel)
            bettingLabelsDraw.append(bettingLabelDraw)
            #time.sleep(0.1)

    #Printing first results:
    print(tabulate(bettingLabels, headers=bettingLabelHeaders, tablefmt="grid"))
    print(tabulate(bettingLabelsBTTS, headers=bettingLabelBTTSHeaders, tablefmt="grid"))
    print(tabulate(bettingLabelsDraw, headers=bettingLabelDrawHeaders, tablefmt="grid"))

    #Terminal application loop - Mainly for sorting data in columns in different ways:
    stop = False
    while stop is not True:
        i = input("Insert index-number to be sorted on or q to quit: ")
        if i == "q":
            stop = True
            break
        index = int(i)
        printNewTableOrder(index, bettingLabels, bettingLabelsBTTS, bettingLabelsDraw)


main()
#eventID, leagueID = Fetch.getLeagueAndEvent("Real Madrid", "Atletico Madrid")
#if (eventID is not None):
    #print("EventID: {} leagueID: {}".format(eventID, leagueID))
    #Fetch.getOdds(leagueID, eventID)
