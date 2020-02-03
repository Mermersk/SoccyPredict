"""
This module simply contains small functions/operations that I need to do,
f.ex: number conversion between different formats.
"""

def fromOddsToDecimalProb(odds):
    return 1 / odds

def fromDecimalProbToOdds(dp):
    return 1 / dp

def fromDecimalProbToPercentage(dp):
    return dp * 100

def fromPercentageToDecimalProb(p):
    return p / 100

def fromPercentageToOdds(p):
    return 100 / p