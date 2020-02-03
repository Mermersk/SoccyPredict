"""
Module contaning the Kelly Criterion formula for determining size of a wager
"""

def kellyCriterion(bankroll, marketOdds, probabilityWinning, fractional):
    """
    Arguments:
        bankroll: float - The current amount in the bank
        marketOdds: float - The markets say presented in odds of probability of x event happening
        probabilityWinning: float - SoccyPredict calculated decimal odds of x event happening. (Range: 0.0 to 1.0)
        fractional: float - fractional is for what kind of Kelly. Full kelly is 1.0 but is risky, other common ones are half, 1/4, 1/8

    Returns:
        betAmount: float - The calculated optimum betting amount to place on wager.
    """

    betAmount = 0.0
    #mo is market odds from MarathonBet
    mo = marketOdds - 1
    #Probability of winning in decimal format
    pw = probabilityWinning
    #probability of losing in decimal format
    pl = 1.0 - pw

    #The percentage of the bankroll to bet, in decimal format!
    betPercentage = ((mo * pw) - pl) / mo
    betPercentage = betPercentage * fractional
    betAmount = round(bankroll * betPercentage, 1)

    print("Bet This Amount: " + str(betAmount))

    return betAmount

#kellyCriterion(67, 1.42, 0.8)