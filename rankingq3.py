from datetime import datetime, timedelta

def winners_dont_lose(table, start, end):
    """
    Creates a ranking system which assigns
    players a score of r if they win in Round r of
    a competition, and subtracts 1/r when they
    lose in Round r of a competition.
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
        # Starting all players with a score of 0.
        j.append(0)
        for i in tournaments:
            if i[10] == j[0]:
                j[1] += i[18]
            # If a player loses, their score is reduced by 1 over the Round they lost in.
            if i[4] == j[0] and i[10] != j[0]:
                j[1]  -= (1/i[18])
            if i[5] == j[0] and i[10] != j[0]:
                j[1] -= (1/i[18])

    return players
