def initializeWeights(players: list[str]) -> list[float]:
    return [1 / len(players) for _ in players]


def updateWeights(
    players: list[str],
    weights: list[float],
    next_player: str,
) -> list[float]:
    index = players.index(next_player)
    update_weight = weights[index] * 0.75 / len(players)
    return [weight + update_weight if idx != index else update_weight for idx, weight in enumerate(weights)]


def updatePlayerCounter(next_player: str, player_select_counter: dict) -> dict:
    if next_player in player_select_counter:
        player_select_counter[next_player] += 1
    else:
        player_select_counter[next_player] = 1
    return player_select_counter
