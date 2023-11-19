import numpy as np
import pandas as pd

def expectancy(win_rate, avg_win, avg_loss) -> float:
    return win_rate * avg_win + (1 - win_rate) * avg_loss

def george(win_rate, avg_win, avg_loss) -> float:
    return (1 + avg_win)**win_rate * (1 + avg_loss)**(1 - win_rate) - 1

def kelly(win_rate, avg_win, avg_loss)-> float:
    return win_rate / np.abs(avg_loss) - (1 - win_rate) / avg_win

def prob(proposition):
    """Computes the probability of a proposition, A."""
    return proposition.mean()

def conditional(proposition, given):
    """Computes the conditional probability of A given B."""
    return prob(proposition[given])