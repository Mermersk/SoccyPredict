import Fetcher as Fetch
import Predict as Predict
import KellyCriterion as Kelly
import Terminal
import Utils

import time

#Global headers for tabulate tables.
bettingLabelHeaders = ["League:", "HomeTeam:", "AwayTeam:", "H - Over 0.5:", "H - O 0.5 M", "HO Diff:", "H Bet $: ", "A - Over 0.5:", "A - O 0.5 M", "AO Diff:", "A Bet $"]#, "1H Over 0.5", "1H Under 0.5:", "H - Under 0.5 Pinny", "A - Under 0.5 Pinny", "H - Diff", "A - Diff"]
bettingLabelBTTSHeaders = ["League:", "HomeTeam:", "AwayTeam:", "BTTS Yes:", "BTTS Yes M:", "BTTS Yes Diff:", "BTTS No:", "BTTS No M:", "BTTS No Diff:"]
bettingLabelDrawHeaders = ["League:", "HomeTeam:", "AwayTeam:", "H Scoring Chance", "A Scoring Chance", "Draw No", "Draw Yes", "Diff Scoring capacity"]

#Global Current Bankroll
bankroll = 79.84

def main():

    #Matches I want to check today, in the format:
    # countryName - String, leagueName - String, howmany - Integer
    todaysMatches = [
        #["Algeria", "Ligue 1", 1],
        #["Hungary", "NB I", 6],
        #["United-Arab-Emirates", "Arabian Gulf League", 3],
        #["Iran", "Persian Gulf Cup", 3],
        #["South-Africa", "Premier Soccer League", 2],
        #["Qatar", "Stars League", 2],
        #["Saudi-Arabia", "Pro League", 3],
        #["Switzerland", "Challenge League", 3],
        #["Spain", "Segunda B - Group 1", 9],
        #["Spain", "Segunda B - Group 2", 7],
        #["Spain", "Segunda B - Group 3", 7],
        #["Spain", "Segunda B - Group 4", 9],
        #["Israel", "Liga Leumit", 3],
        #["Italy", "Serie C", 1],
        #["France", "Ligue 2", 1],
        #["France", "Ligue 1", 3],
        #["France", "National", 8],
        #["Switzerland", "Super League", 3],
        #["Northern-Ireland", "Championship", 2],
        #["Scotland", "League One", 5],
        #["Scotland", "League Two", 5],
        
        #["Portugal", "Liga de Honra", 3],
        #["Portugal", "Primeira Liga", 5],
         
        #["Egypt", "Premier League", 2],
        
        #["Cyprus", "1. Division", 1],
        #["Germany", "Bundesliga 2", 1],
        ["Germany", "Bundesliga 1", 2],
        #["Germany", "Liga 3", 1],
        #["Spain", "Primera Division", 6],
        #["Spain", "Segunda Division", 6],
        #["Egypt", "Premier League", 2],
        #["Belgium", "Jupiler Pro League", 3],
        #["Israel", "Ligat ha'Al", 1],
        
        #["Netherlands", "Eerste Divisie", 2],
        #["Netherlands", "Eredivisie", 4],
        #["Scotland", "Championship", 4],
        #["Scotland", "Premiership", 1],
        #["Italy", "Serie A", 1],
        
        #["Italy", "Serie B", 1],

        #["Greece", "Super League", 4],
        #["India", "Indian Super League", 1],
        #["England", "Championship", 10],
        #["England", "League One", 11],
        #["England", "League Two", 12],
        #["England", "National League", 12],
        #["England", "Premier League", 2],
        

        
        #["Oman", "Professional League", 2],

        #["Turkey", " Super Lig", 1],
        #["Turkey", "TFF 1. Lig", 1],
        
        #["Australia", "A-League", 1],

    ]

    bettingLabels = []
    bettingLabelsBTTS = []
    bettingLabelsDraw = []

    #Should tell me which matches were skipped - No odds were available on the market for it
    skippedMatches = []
    
    for match in todaysMatches: 
        
        upcomingLeagueFixtures = Fetch.getUpcomingFixturesForLeague(match[0], match[1], match[2])

        for fixture in upcomingLeagueFixtures:
            allLabels = Predict.predictOne(match[0], match[1], fixture[0], fixture[1])
            bettingLabel = allLabels[0]
            bettingLabelBTTS = allLabels[1]
            bettingLabelDraw = allLabels[2]

            marketOdds, marketOddsBTTS = Fetch.getScoringOdds(fixture[2])

            #if not marketOdds, will detect if list is empty! If not available, then dont make a label for that fixture
            if not marketOdds:
                skippedMatches.append("{} vs {} Was skipped(No market odds)".format(fixture[0], fixture[1]))
                continue
           
            bettingLabel.insert(4, marketOdds[0])
            bettingLabel.insert(5, float(marketOdds[0]) - bettingLabel[3])
            #Inserting bet amount here based on kelly criterion formula
            betAmount = Kelly.kellyCriterion(bankroll, float(marketOdds[0]), Utils.fromOddsToDecimalProb(bettingLabel[3]), 0.25)
            bettingLabel.insert(6, betAmount)

            #bettingLabel.insert(8, marketOdds[1])
            #bettingLabel.insert(9, float(marketOdds[1]) - bettingLabel[7])
            bettingLabel.insert(8, marketOdds[2])
            bettingLabel.insert(9, float(marketOdds[2]) - bettingLabel[7])

            betAmount = Kelly.kellyCriterion(bankroll, float(marketOdds[2]), Utils.fromOddsToDecimalProb(bettingLabel[7]), 0.25)
            bettingLabel.insert(10, betAmount)

            #bettingLabel.insert(15, marketOdds[3])
            #bettingLabel.insert(16, float(marketOdds[3]) - bettingLabel[14])

            bettingLabelBTTS.insert(4, marketOddsBTTS[0])
            
            bettingLabelBTTS.insert(5, float(marketOddsBTTS[0]) - bettingLabelBTTS[3])
            bettingLabelBTTS.insert(7, marketOddsBTTS[1])
            bettingLabelBTTS.insert(8, float(marketOddsBTTS[1]) - bettingLabelBTTS[6])

            bettingLabelsBTTS.append(bettingLabelBTTS)
            bettingLabels.append(bettingLabel)
            bettingLabelsDraw.append(bettingLabelDraw)
            #time.sleep(0.1)

    #Printing first results:
    Terminal.display(bettingLabels, bettingLabelHeaders)
    Terminal.display(bettingLabelsBTTS, bettingLabelBTTSHeaders)
    Terminal.display(bettingLabelsDraw, bettingLabelDrawHeaders)

    #Gathering absolutely all labels generated to sed to Terminal Module
    labels = [bettingLabels, bettingLabelsBTTS, bettingLabelsDraw]
    Terminal.getAllLabels(labels)
    labelHeaders = [bettingLabelHeaders, bettingLabelBTTSHeaders, bettingLabelDrawHeaders]
    Terminal.getAllLabelsHeaders(labelHeaders)

    print(skippedMatches)

    Terminal.appLoop()


main()







