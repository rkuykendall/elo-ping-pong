import operator
from elo import Rating, rate_1vs1


def ranking(matches, start=1000):
    players = {}

    for match in matches:
        winner = match.winner
        loser = match.loser

        if winner not in players:
            players[winner] = Rating(start)

        if loser not in players:
            players[loser] = Rating(start)

        new_winner, new_loser = rate_1vs1(players[winner], players[loser])
        players[winner] = new_winner
        players[loser] = new_loser

    sorted_players = sorted(
        players.items(), key=operator.itemgetter(1))
    sorted_players.reverse()
    sorted_players = [
        {'player': p, 'score': int(s)} for p, s in sorted_players]

    return sorted_players
