import csv
from datetime import datetime, timedelta

def update_data(file):
    """This function imports the csv, storing
    each match as list within a list."""

    data = []
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data.append(row)
    return data

def winners(rows):
    """Splits the string scores into
    6 individual columns to compare set
    scores and determine the winner
    of each match."""

    for i in rows:
        # Dividing round scores into individual columns for each player.
        i[12:13] = i[8].split('-')
        i[14:15] = i[9].split('-')

        # if the third set was not played, the scores for the players are set to 0.
        if i[10] == '':
            i.append('0')
            i.append('0')
        else:
            i[16:17] = i[10].split('-')

        # some rows are shorter if a player retired.
        # Extending all lists to be the same length: 18.
        if len(i) == 16:
            i.append('')
            i.append('')
        if len(i) == 17:
            i.append('')

        # Calculating winners
        # Replacing old columns with the set scores for each player.
        i[8] = 0
        i[9] = 0
        try:
            if int(i[12]) > int(i[13]):
                i[8] += 1
            if int(i[12]) < int(i[13]):
                i[9] += 1
            if int(i[14]) > int(i[15]):
                i[8] += 1
            if int(i[14]) < int(i[15]):
                i[9] += 1
            if int(i[16]) > int(i[17]):
                i[8] += 1
            if int(i[16]) < int(i[17]):
                i[9] += 1
        except (ValueError):
            pass

        # Setting the old column i[10] to hold the name of the winner.
        if i[8] > i[9]:
            i[10] = i[4]
        else:
            i[10] = i[5]

        # Some matches have no score recorded as one player retired.
        # Their name will be in the notes, therefore making the other
        # player the winner.
        if i[11] != 'Completed':
            if i[4] in i[11]:
                i[10] = i[5]
            else:
                i[10] = i[4]

    return rows

def date_time(rows, i1, i2):
    """Takes a dataset and updates
    the 2 columns to reformat from a string
    to datetime format"""
    for i in rows:
        i[i1] = datetime.strptime(i[i1], "%Y-%m-%d")
        i[i2] = datetime.strptime(i[i2], "%Y-%m-%d")

    return rows

def rounds(rows):
    """Takes a dataset of matches played in Tournaments
    and determines which round each match was played in,
    based on the number of times a player won to reach
    each match."""
    # Takes Tournament names from each row of data.
    Tournaments = []
    for i in rows:
        Tournaments.append([i[0],i[1].year])

        # Creating space for new variables.
        i.append(0)
        i.append('')

    # Transforms into a dictionary, to preserve the order
    # of the tournaments in terms of date, and returns a list
    Tournaments = list(dict.fromkeys([tuple(x) for x in Tournaments]))

    # empty list to store list of lists of all rounds played to correspond to Tournaments.
    maxrounds = []

    # Iterates through each tournament
    for j in range(0, len(Tournaments)):

        # Index of which match in the tournament we are observing
        k = 0
        # Empty list to store winners for each match in each tournament
        Winners = []
        # Empty list to store the rounds for each tournament
        rounds = []
        # Appends to maxrounds for each tournament.
        maxrounds.append(rounds)

        # Iterating through the rows to find all rows which correspond to Tournaments[j]
        for i in rows:

            if i[0] == Tournaments[j][0] and i[1].year == Tournaments[j][1]:
                Winners.append(i[10])
                k += 1

                # Counting how many times each player has won a match prior to this game to determine the round.
                p1 = Winners[0:k-1].count(i[4])
                p2 = Winners[0:k-1].count(i[5])

                # if i[0] in list.
                if i[0] == 'Sony Ericsson Championships' or i[0] == 'Commonwealth Bank Tournament of Champions' and i[1].year == 2009 or i[0] == 'Qatar Airways Tournament of Champions Sofia' or i[0] == 'Garanti Koza WTA Tournament of Champions' or i[0] == 'BNP Paribas WTA Finals' or i[0] == 'WTA Elite Trophy' or i[0] == 'WTA Finals':
                    if len(Winners[0:k-1]) <= 11 :
                        i[18] = 1
                    if len(Winners[0:k-1]) == 12 or len(Winners[0:k-1]) == 13:
                        i[18] = 2
                    if len(Winners[0:k-1]) == 14:
                        i[18] = 3


                # Some players enter in later rounds, therefore we take the maximum of the two.
                # Adding 1 as in round 1 players have won 0 times.
                else:
                    i[18] = max([p1,p2]) + 1

                rounds.append(i[18])

    # Taking the maximum round for each tournament
    maximum = []
    for i in maxrounds:
        maximum.append(max(i))

    # Making a new column which identifies Finals and Rounds.
    for j in range(0, len(Tournaments)):
        for i in rows:
            if i[0] == Tournaments[j][0] and i[1].year == Tournaments[j][1]:
                if i[0] == 'Sony Ericsson Championships' or i[0] == 'Commonwealth Bank Tournament of Champions' and i[1].year == 2009 or i[0] == 'Qatar Airways Tournament of Champions Sofia' or i[0] == 'Garanti Koza WTA Tournament of Champions' or i[0] == 'BNP Paribas WTA Finals' or i[0] == 'WTA Elite Trophy' or i[0] == 'WTA Finals':
                    if i[18] == maximum[j]-2:
                        i[19] == ''
                else:
                    if i[18] == maximum[j]-2:
                        i[19] = 'Quarter-Final'
                if i[18] == maximum[j]-1:
                    i[19] = 'Semi-Final'
                if i[18] == maximum[j]:
                    i[19] = 'Final'
                if i[19] == '':
                    i[19] = 'Round ' + str(i[18])

    return rows

def finalwinner(data, Tournament, year):
    """Takes a Tournament and a year and
    returns the winner of the final."""
    for i in data:
        if i[19] == 'Final' and i[0] == Tournament and i[1].year == year:
            winner = i[10]

    return str(winner) + " won the final of the " + str(year) + " " + str(Tournament)

def roundsplayers(data, Tournament, year, round):
    """Takes a Tournament, year and round, and
    returns the matches played in that round
    of the tournament."""
    matches = []
    for i in data:
        if i[18] == round and i[0] == Tournament and i[1].year == year:
            matches.append([i[4], 'vs', i[5]])

    return matches


def roundelimination(data, Tournament, year, player):
    """Takes a player, tournament and year, and returns
    the round in which that player was eliminated."""
    rounds = []
    for i in data:
        if i[0] == Tournament and i[1].year == year:
            if i[10] == player:
                rounds.append(i[18])
    round = max(rounds) + 1
    return str(player) + " was eliminated in Round " + str(round) + " of the " + str(year) + " " + str(Tournament)

def nofinals(data, player):
    """Takes a players name and returns the
    #number of finals in which they have played"""
    finals = 0
    for i in data:
        if i[19] == 'Final' and i[4] == player:
            finals += 1
        if i[19] == 'Final' and i[5] == player:
            finals += 1

    return str(player) + " has played in " + str(finals) + " finals until now."

def who_won(data, player1, player2):
    """Takes 2 players and returns their total
    number of matches and how many matches each
    player has won."""
    total_matches = 0
    player1_won = 0
    player2_won = 0

    for i in data:
        if i[4] == player1 and i[5] == player2:
            total_matches += 1
            if i[10] == player1:
                player1_won += 1
            else:
                player2_won += 1
        if i[4] == player2 and i[5] == player1:
            total_matches += 1
            if i[10] == player1:
                player1_won += 1
            else:
                player2_won += 1

    return str(player1) + " and " + str(player2) + " played against each other " + str(total_matches) + " times. " + str(player1) + " has won " + str(player1_won) + " times. " + str(player2) + " has won " + str(player2_won) + " times."
