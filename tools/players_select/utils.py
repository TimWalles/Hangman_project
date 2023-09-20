import os
import random

operation_settings = {
    'help': 'displays input variables to set and change the player selector',
    'list': 'list all players',
    'add': 'add player - "add <player_name>" or  - "add <player_name1,player_name2,...>"',
    'remove': 'remove player - "remove <player_name>" or "remove <player_name1,player_name2,...>"',
    'stop': 'stops player select',
}


# region operations
def listHelpOperations(operation_settings: dict):
    print('\n\n')
    for operation, desc in operation_settings.items():
        print(f'{operation} : {desc} ')
    print('\n\n')


def addPlayer(player_name: str, players: list[str]) -> list[str]:
    new_players = player_name.split(',')
    new_players = [name.capitalize() for name in new_players]
    print(f'\n\nPlayer(s) {", ".join(new_players)} are added to the players list.')
    return players + new_players


def removePlayer(player_name: str, players: list[str]) -> list[str]:
    player_name = player_name.capitalize()
    try:
        players.remove(player_name)
        print(f'\n\nPlayer {player_name} as been removed from the players list.')
    except ValueError:
        print(f'\n\nNo player with name {player_name} in players list. Type list to see all players')
    return players


def listPlayers(players):
    print('\n\nListed players are:\n')
    for player in players:
        print(f'{player}\n')


def stopPlayerSelect(player_select_counter) -> bool:
    print('Stopping player select!')
    printPlayerCount(player_select_counter)
    return False


def printPlayerCount(player_select_counter: dict):
    for player, count in player_select_counter.items():
        print(f'Player {player.capitalize()} played: {count} times.')


# endregion
