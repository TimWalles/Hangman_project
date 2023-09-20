import os

from tools.players_select.selection_logic import *
from tools.players_select.utils import *

players = [
    'Aisha',
    'Alla',
    'Anurag',
    'Kate',
    'Katie',
    'Lisardo',
    'Moritz',
    'Noah',
    'Philipp',
    'Prabha',
    'Sanja',
]
weights = []
pick_player = True
player_select_counter = {}

i = 0
os.system('clear')
while pick_player:
    if i == 0:
        user_input = input('Hit [ENTER] to pick a player,\n\nOR type "stop" to stop or "help" for addition settings: ').lower().split(' ', 1)
    else:
        user_input = input('Hit [ENTER] to pick a player: ').lower().split(' ', 1)

    if not user_input[0]:
        if i == 0:
            weights = initializeWeights(players)
            i += 1
        os.system('clear')
        next_player = random.choices(players, weights=weights, k=1)[0]
        print(f'Next player is: {next_player}\n')
        weights = updateWeights(players, weights, next_player)
        player_select_counter = updatePlayerCounter(next_player, player_select_counter)
        continue
    elif user_input[0] in operation_settings:
        match user_input[0]:
            case 'help':
                listHelpOperations(operation_settings)
            case 'list':
                listPlayers(players)
            case 'add':
                players = addPlayer(user_input[1], players)
            case 'remove':
                players = removePlayer(user_input[1], players)
            case 'stop':
                pick_player = stopPlayerSelect(player_select_counter)

    else:
        print(f'\nInput error: input {user_input} is not recognized. Please type "help" to see additional settings\n')
        continue
