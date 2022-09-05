from datetime import datetime, timedelta

def WbW(table, start, end):

    """
    Ranks players based on a Winners beat other
    Winners system: a player's score is increased by more if
    they win against a player with a higher ranking, and who
    has lost less games.
    """

    # Empty list to store rankings
    players = []
    tournaments = []
    for i in table:
        if i[1] > start and i[1] < end:
            tournaments.append(i)

    # append all players of all matches in the period
    for i in tournaments:
        players.append(i[4])
        players.append(i[5])

    # Remove duplicates for a list of unique players
    players = list(set(players))

    # Making a list of lists
    players = [[i] for i in players]

    # Assigning them a score of 1/n
    n = len(players)
    for j in players:
        j.append(1/n)

    # the player at the top of the list is randomly assigned as the player whose score
    # we will use to set the convergence criteria.
    converge_player = players[0][0]
    # Each time the process repeats itself, 1 players score is appended to a list for comparison
    converge = []
    # Indexes which iteration we are at.
    p = 0

    # Could see if top and bottom 3 doesnt change.
    def step2(players, p):
        """Takes scores assigned to players,
        divides this score by the number of
        players they have lost to, and passes
        this amount to the player which they
        lost to."""
        p += 1
        # if the function has run 3 times, and there is a difference of less than
        # 0.00001 between Williams current score and her previous, the procedure stops.
        if p > 3 and abs(converge[p-2] - converge[p-3]) < 0.0000001:
            return players
        else:
            for j in players:
                j.append([])
                j.append(0)
                for i in tournaments:
                    # If the player played a match but was not the winner,
                    # we append the winning opponent's name to a list of all the player's
                    # opponents who won.
                    if i[4] == j[0] and i[10] != j[0]:
                        j[2].append([i[5]])
                    if i[5] == j[0] and i[10] != j[0]:
                        j[2].append([i[4]])

            for i in players:
                # If the player never lost, their name is in the list of winning opponents,
                # for their score to be passed to themself.
                if len(i[2]) == 0:
                    i[2].append([i[0]])

                # Divide the player's score by their number of winning opponents
                try:
                    i[3] = i[1]/len(i[2])
                except (ZeroDivisionError):
                    pass
                # Append this score to each winning opponent.
                for j in i[2]:
                    j.append(i[3])


            # Extract this list of winning opponents with their new scores into a new list.
            # Players will have scores in here for every match they have won.
            allscores = []
            for i in players:
                for j in i[2]:
                    allscores.append(j)

            # if a player has won no games, they will not have been passed a score,
            # they must be appended to the dataset with a score of 0
            for i in players:
                if i[0] not in allscores:
                    allscores.append([i[0], 0])

            # To sum all scores for each player, we create a dictionary where
            # the key is the player and the value is a list of all scores passed onto them.
            dic = {}
            for key,val in allscores:
                dic.setdefault(key,[]).append(val)

            # Sum all of these scores to create a single value for each player.
            scores = {k: sum(dic[k]) for k in dic.keys()}

            # Transform to a list.
            scores = [[k, v] for k, v in scores.items()]

            # Adjust scores to score*0.85 + 0.15/n as instructed.
            for i in scores:
                i[1] = i[1]*0.85 + 0.15/n

                # Append top score for comparison.
                if i[0] == converge_player:
                    converge.append(i[1])

            # you need to include all the players in the final list bc. +.15/n
            return step2(scores,p)

    return step2(players, p)
