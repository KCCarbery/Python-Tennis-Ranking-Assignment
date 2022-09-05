from datetime import datetime, timedelta
from rankingq4 import WbW
import matplotlib
from matplotlib import pyplot

def update_rankings(table, start, end):
    """Adds 2 new rows to the original data
    to store rankings for player 1 and player 2
    for each match, and adds the scores between 2
    specified dates."""
    rankings = WbW(table, start, end)

    # 2 new rows to store the rankings
    for i in table:
        i.append(0)
        i.append(0)
        for j in rankings:
            # Updating the scores based on the rankings from WbW
            if i[4] == j[0] and i[1] >= start and i[1] <= end:
                i[20] = j[1]
            if i[5] == j[0] and i[1] >= start and i[1] <= end:
                i[21] = j[1]
    return table

def comparing_scores(table, cutoff):
    """Takes the table, and updates the scores of
    players in each tournament, based on all total_matches
    which have occurred in the previous year."""
    tournament = []
    for i in table:
        if i[1] >= cutoff:
            tournament.append(i)


    first = tournament[0][0]
    year = tournament[0][1].year
    for i in tournament:
        if i[0] == first:
            pass
        # need to update first tournament
        if i[0] != first:
            first = i[0]
            year = i[1].year
            rank = WbW(table, i[1] - timedelta(days=365), i[1])
            for j in rank:
                for k in table:
                    if k[4] == j[0] and k[0] == first and k[1].year == year:
                        k[20] = j[1]
                    if k[5] == j[0] and k[0] == first and k[1].year == year:
                        k[21] = j[1]


    return table

def matplot(data, start):
    """Takes the dataset, extracts relevant
    scores, reduces the data to be a unique
    point for each time a player has played
    a tournament, and plots"""
    rankings = []
    for i in data:
        if i[1] >= start:
            rankings.append([i[0], i[1], i[4], i[6], i[20]])
            rankings.append([i[0], i[1], i[5], i[7], i[21]])

    rankings = [list(x) for (x) in set([tuple(x) for x in rankings])]

    # Updating WTA rankings to floats instead of strings.
    for i in rankings:
        if i[3] == '':
            i[3] = None
        else:
            i[3] = float(i[3])

    plot = matplotlib.pyplot.scatter(x = [i[3] for i in rankings], y = [i[4] for i in rankings])

    return plot
