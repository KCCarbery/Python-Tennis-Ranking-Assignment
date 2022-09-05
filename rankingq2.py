from datetime import datetime, timedelta
import datetime

def winnerswin(table, start, end):
    """
    Takes tennis data, a start and end
    date, and returns a ranking for players in
    the data by counting how many matches they have won
    between these two dates.
    """

    # Empty list to store rankings
    players = []
    tournaments = []
    for i in table:
        if i[1] >= start and i[1] <= end:
            tournaments.append(i)

    # append all players of all matches in the period
    for i in tournaments:
        players.append(i[4])
        players.append(i[5])

    # Remove duplicates for a list of unique players
    players = list(set(players))

    # Making a list of lists
    players = [[i] for i in players]

    for j in players:
        j.append(0)
        for i in tournaments:
            if i[10] == j[0]:
                j[1] += 1

    return players
