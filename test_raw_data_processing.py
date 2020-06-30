import unittest
from raw_data_processing import parse_single_game, group_game_list_ECO

class TestRawDataProcessing(unittest.TestCase):
    def setUp(self):
        self.valid_game_pgn = "[Event \"4. IIFL Wealth Mumbai Op\"][Site \"Mumbai IND\"][Date \"2018.12.31\"][Round \"2.9\"][White \"Sundararajan, Kidambi\"][Black \"Ziatdinov, Raset\"][Result \"1/2-1/2\"][WhiteElo \"2458\"][BlackElo \"2252\"][ECO \"A25\"][EventDate \"2018.12.30\"]1.c4 e5 2.Nc3 Nc6 1/2-1/2"
        self.valid_game_dict = {
            'Date': '2018.12.31',
            'Round' : '2.9',
            'White': 'Sundararajan, Kidambi',
            'Black': 'Ziatdinov, Raset',
            'Result': '1/2-1/2',
            'WhiteElo': '2458',
            'BlackElo' :'2252',
            'ECO':'A25',
            'EventDate' : '2018.12.30',
            'Game': '1.c4 e5 2.Nc3 Nc6 1/2-1/2'
        }

        test_game_1 = {'ECO': 'A20', 'Game' : '1.e4 e5 1/2-1/2'}
        test_game_2 = {'ECO': 'B23', 'Game' : '1.e4 c5 0-1'}
        test_game_3 = {'ECO': 'A20', 'Game' : '1.b3 1-0'}
        self.group_test_games = [test_game_1, test_game_2, test_game_3]
        self.group_test_games_dict = {
            'A20': [{'ECO': 'A20', 'Game' : '1.e4 e5 1/2-1/2'},{'ECO': 'A20', 'Game' : '1.b3 1-0'}],
            'B23':[{'ECO': 'B23', 'Game' : '1.e4 c5 0-1'}]
        }
        
    def test_parse_single_game_valid(self):
        parsed = parse_single_game(self.valid_game_pgn)
        self.assertDictEqual(parsed,self.valid_game_dict)
    
    def test_parse_single_game_invalid(self):
        with self.subTest():
            not_a_pgn = 'Hello There'
            self.assertRaises(ValueError, parse_single_game, not_a_pgn)
        with self.subTest():
            missing_ECO = "[Event \"4. IIFL Wealth Mumbai Op\"][Site \"Mumbai IND\"][Date \"2018.12.31\"]"
            self.assertRaises(ValueError, parse_single_game, missing_ECO)
        with self.subTest():
            missingGame = "[Event \"4. IIFL Wealth Mumbai Op\"][Site \"Mumbai IND\"][ECO \"A25\"]"
            self.assertRaises(ValueError, parse_single_game, missingGame)

    def test_group_game_list_ECO(self):
        grouped = group_game_list_ECO(self.group_test_games)
        self.assertDictEqual(grouped, self.group_test_games_dict)



if __name__ == '__main__':
    unittest.main()
