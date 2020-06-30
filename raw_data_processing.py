"""
Convert the Kingbase .pgn files into a parsed format.
Store in a pickle, grouped by openning ECO code

Kingbase database: https://www.kingbase-chess.net/
ECO code: https://en.wikipedia.org/wiki/List_of_chess_openings
"""

import os
from collections import Counter
import pickle

def parse_single_game(game_str):
    """parse the .pgn string for a single game into a dict
    The 'Event' and 'Site' tags are discarded.

    
    Parameters
    ----------
    game_str : string
        .pgn descriptor of the game
    """
    ESSENTIAL_KEYS = ['ECO', 'Game']
    game_fields = game_str.split(']')
    game_dict = {}
    for field in game_fields[2:-1]: #Discard 'Event' and 'Loc'
        temp = field.split()
        key = temp[0][1:]
        val = ' '.join(temp[1:])[1:-1] # Discard quotation marks
        game_dict[key] = val
    game_dict['Game'] = game_fields[-1]
    for key in ESSENTIAL_KEYS:
        if not key in game_dict.keys():
            raise ValueError
    if len(game_dict['Game'])==0:
        raise ValueError
    return(game_dict)

def create_list_all_games(directory):
    """Add all games from pgn files in a directory to a list
    
    Parameters
    ----------
    directory : str
        data directory
    
    Returns
    -------
    list(dict)
        A list of dicts, each corresponding to a game in the directory
    """
    all_game_list = []
    for file in os.listdir(directory):
        if file.endswith(".pgn"):
            filename = os.path.join(directory, file)
            print(filename)
            with open(filename, 'r', encoding = 'ISO-8859-1') as file:
                data = file.read().replace('\n', '')
            
            games = data.split('[Event ')
            for i,g in enumerate(games[1:]):
                if i%30000 == 0:
                    print(i, ' games parsed')
                    
                all_game_list.append(parse_single_game(g))
    return all_game_list

def group_game_list_ECO(game_list):
    """Group games from the list by ECO code
    
    Parameters
    ----------
    game_list : list (dict)
        list of parsed individual games
    
    Returns
    -------
    dict
        dict{ECO:[game list]}
    """
    gamedict_by_eco = {}
    for game in game_list:
        if gamedict_by_eco.get(game['ECO']) is None:
            gamedict_by_eco[game['ECO']] = [game]
        else:
            gamedict_by_eco[game['ECO']].append(game)
    return gamedict_by_eco

def dump_to_pickle(outfilename, data):
    with open(outfilename, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    all_game_list = create_list_all_games('./data/')
    game_dict = group_game_list_ECO(all_game_list)
    dump_to_pickle('all_processed_data.pkl', game_dict)