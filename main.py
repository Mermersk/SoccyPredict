import Fetcher as Fetch
import Predict as Predict
import KellyCriterion as Kelly
import Terminal
import Utils

import time

#Global headers for tabulate tables.
bettingLabelHeaders = ["League:", "HomeTeam:", "AwayTeam:", "H - Over 0.5:", "H - O 0.5 M", "HO Diff:", "H Bet $: ", "A - Over 0.5:", "A - O 0.5 M", "AO Diff:", "A Bet $"]#, "1H Over 0.5", "1H Under 0.5:", "H - Under 0.5 Pinny", "A - Under 0.5 Pinny", "H - Diff", "A - Diff"]
bettingLabelBTTSHeaders = ["League:", "HomeTeam:", "AwayTeam:", "BTTS Yes:", "BTTS Yes M:", "BTTS Yes Diff:", "BTTS No:", "BTTS No M:", "BTTS No Diff:"]
bettingLabelDrawHeaders = ["League:", "HomeTeam:", "AwayTeam:", "Diff for draw: "]
bettingLabelDCHeaders = ["League:", "HomeTeam:", "AwayTeam:", "HomeTeam DC", "H-DC-M", "H Diff", "AwayTeam DC", "A-DC-M", "A Diff"]
#Global Current Bankroll
bankroll = 106.67

def main():

    #Matches I want to check today, in the format:
    # countryName - String, leagueName - String, howmany - Integer
    todaysMatches = [
        ["Norway", "Eliteserien", 2]
        #["England", "National League - South", 2],
        #["Denmark", "Superligaen", 1],
        #["Denmark", "Viasat Divisionen", 2],
        #["Iran", "Azadegan League", 9],
        #["Qatar", "2nd Division League", 4],
        #["Saudi-Arabia", "Division 1", 5],
        #["England", "National League - North", 4],
        #["Tunisia", "Ligue Professionnelle 1", 3],
        #["India", "I-League", 2],
        #["Morocco", "Botola Pro", 2],
        #["Algeria", "Ligue 1", 5],
        #["Algeria", "Ligue 2", 7],
        #["Hungary", "NB I", 6],
        #["United-Arab-Emirates", "Arabian Gulf League", 4],
        #["Poland", "Ekstraklasa", 4],
        #["Iran", "Persian Gulf Cup", 6],
        #["South-Africa", "Premier Soccer League", 3],
        #["Qatar", "Stars League", 2],
        
        #["Saudi-Arabia", "Pro League", 3],
        #["Switzerland", "Challenge League", 1],
        #["Spain", "Segunda B - Group 1", 6],
        #["Spain", "Segunda B - Group 2", 5],
        #["Spain", "Segunda B - Group 3", 6],
        #["Spain", "Segunda B - Group 4", 9],
        #["Israel", "Liga Leumit", 5],
        #["Italy", "Serie C", 9],
        #["France", "Ligue 2", 8],
        #["France", "Ligue 1", 6],
        #["France", "National", 9],
        #["Switzerland", "Super League", 2],
        #["Northern-Ireland", "Championship", 2],
        #["Northern-Ireland", "Premiership", 4],
        #["Scotland", "League One", 5],
        #["Scotland", "League Two", 5],
        
        #["Portugal", "Liga de Honra", 2],
        #["Portugal", "Primeira Liga", 3],
         
        #["Egypt", "Premier League", 1],
        
        #["Cyprus", "1. Division", 2],
        #["Germany", "Bundesliga 2", 2],
        #["Germany", "Bundesliga 1", 6],
        #["Germany", "Liga 3", 1],
        #["Spain", "Primera Division", 3],
        #["Spain", "Segunda Division", 5],
        #["Egypt", "Premier League", 1],
        #["Belgium", "Jupiler Pro League", 8],
        #["Israel", "Ligat ha'Al", 3],
        
        #["Netherlands", "Eerste Divisie", 6],
        #["Netherlands", "Eredivisie", 4],
        #["Scotland", "Championship", 5],
        #["Scotland", "Premiership", 5],
        #["Italy", "Serie A", 1],
        
        #["Italy", "Serie B", 6],

        #["Greece", "Super League", 1],
        #["India", "Indian Super League", 1],
        #["England", "Championship", 9],
        #["England", "League One", 11],
        #["England", "League Two", 11],
        #["England", "National League", 12],
        #["England", "Premier League", 6],
        
        
        #["Oman", "Professional League", 2],

        #["Turkey", " Super Lig", 3],
        #["Turkey", "TFF 1. Lig", 3],
        #["Turkey", "TFF 2. Lig", 15],
        
        #["Australia", "A-League", 1],

    ]

    bettingLabels = []
    bettingLabelsBTTS = []
    bettingLabelsDraw = []
    bettingLabelsDC = []

    #Should tell me which matches were skipped - No odds were available on the market for it
    skippedMatches = []
    
    for match in todaysMatches: 
        
        upcomingLeagueFixtures = Fetch.getUpcomingFixturesForLeague(match[0], match[1], match[2])

        for fixture in upcomingLeagueFixtures:
            allLabels = Predict.predictOne(match[0], match[1], fixture[0], fixture[1])
            bettingLabel = allLabels[0]
            bettingLabelBTTS = allLabels[1]
            bettingLabelDraw = allLabels[2]
            bettingLabelDC = allLabels[3]

            marketOdds, marketOddsBTTS = Fetch.getScoringOdds(fixture[2])
            homeDCOdds, awayDCOdds = Fetch.getDCOdds(fixture[2])
            

            bettingLabelDC.insert(4, homeDCOdds)
            bettingLabelDC.insert(7, awayDCOdds)
            if (homeDCOdds == 0.0 or awayDCOdds == 0.0):
                bettingLabelsDC.append(bettingLabelDC)
                continue

              #-------------------------Double chance insertions here
            print("{} |||||||| {}".format(homeDCOdds, bettingLabelDC[3]))
            print("{} |||||||| {}".format(awayDCOdds, bettingLabelDC[6]))
            
            bettingLabelDC.insert(5, float(homeDCOdds) - float(bettingLabelDC[3]))
            bettingLabelDC.insert(8, float(awayDCOdds) - float(bettingLabelDC[6]))

            bettingLabelsDC.append(bettingLabelDC)

            #if not marketOdds, will detect if list is empty! If not available, then dont make a label for that fixture
            if not marketOdds:
                skippedMatches.append("{} vs {} Was skipped(No market odds)".format(fixture[0], fixture[1]))
                continue
           
            #bettingLabel.insert(4, marketOdds[0])
            #bettingLabel.insert(5, float(marketOdds[0]) - bettingLabel[3])
            #Inserting bet amount here based on kelly criterion formula
            #betAmount = Kelly.kellyCriterion(bankroll, float(marketOdds[0]), Utils.fromOddsToDecimalProb(bettingLabel[3]), 0.125)
            #bettingLabel.insert(6, betAmount)

            #bettingLabel.insert(8, marketOdds[1])
            #bettingLabel.insert(9, float(marketOdds[1]) - bettingLabel[7])
            #bettingLabel.insert(8, marketOdds[2])
            #bettingLabel.insert(9, float(marketOdds[2]) - bettingLabel[7])

            #betAmount = Kelly.kellyCriterion(bankroll, float(marketOdds[2]), Utils.fromOddsToDecimalProb(bettingLabel[7]), 0.125)
            #bettingLabel.insert(10, betAmount)

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

    #print(bettingLabelsDC)
    #Printing first results:
    Terminal.display(bettingLabels, bettingLabelHeaders)
    Terminal.display(bettingLabelsBTTS, bettingLabelBTTSHeaders)
    Terminal.display(bettingLabelsDraw, bettingLabelDrawHeaders)

    Terminal.display(bettingLabelsDC, bettingLabelDCHeaders)

    #Gathering absolutely all labels generated to sed to Terminal Module
    labels = [bettingLabels, bettingLabelsBTTS, bettingLabelsDraw, bettingLabelsDC]
    Terminal.getAllLabels(labels)
    labelHeaders = [bettingLabelHeaders, bettingLabelBTTSHeaders, bettingLabelDrawHeaders, bettingLabelDCHeaders]
    Terminal.getAllLabelsHeaders(labelHeaders)

    print(skippedMatches)

    Terminal.appLoop()


main()







