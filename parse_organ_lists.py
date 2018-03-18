
import pandas as pd

def parser(filename):
    """
    Takes in a filename.
    Returns a Pandas DataFrame representing a list of organs.
    """
    return pd.read_csv(filename, parse_dates=['ArrivalDate'])
