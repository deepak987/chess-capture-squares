import unittest
from opening_analyzer import OpeningCaptureAnalyzer
from collections import Counter
import numpy as np 
import pickle

class TestOpeningAnalyzer(unittest.TestCase):

    def setUp(self):
         with open('all_processed_data.pkl', 'rb') as handle:
            game_dict_openings = pickle.load(handle)

            self.analyzer = OpeningAnalyzer(game_dict_openings)

    def test_get_capture_squares(self):
        with self.subTest():
            valid_pgn_capture = 'hello 1.e4 e5 2.d4 exd4 3.c3 dxc3'
            captures = self.analyzer.get_capture_squares(valid_pgn_capture)
            self.assertCountEqual(['c3', 'd4'], captures) #assertCountEqual checks that the lists are the same, order not checked
        with self.subTest():
            valid_pgn_no_capture = 'hello 1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5'
            captures = self.analyzer.get_capture_squares(valid_pgn_no_capture)
            self.assertListEqual([], captures)
        
        with self.subTest():
            invalid_pgn_capture = 'hello 1.e4 e5 2.Nf3 Nc6 3.Bc4 Bxc9'
            captures = self.analyzer.get_capture_squares(invalid_pgn_capture)
            self.assertListEqual([], captures)


    def test_counter_to_array(self):
        square_list = ['e4', 'a1', 'a1']
        sq_counter = Counter(square_list)
        correct_board = np.zeros((8,8))
        correct_board[4][4] = 1
        correct_board[7,0] = 2
        parsed_board = self.analyzer.counter_to_array(sq_counter)
        
        self.assertEqual(np.all(parsed_board==correct_board), True)

    def test_create_capture_board(self):

        with self.subTest():
            self.assertRaises(KeyError, self.analyzer.create_capture_board, 'Z24')

    def test_get_piece_move_freq(self):
        with self.subTest():
            empty_counter = Counter({'P':0, 'K':0,'N':0,'R':0,'B':0,'Q':0})
            self.assertDictEqual(empty_counter, self.analyzer.get_piece_move_freq(''))

        with self.subTest():
            pgn = '1.e4 e5 2.d4 exd4 3.c3 dxc3 1-0'
            counter = Counter({'P':6, 'K':0,'N':0,'R':0,'B':0,'Q':0})

            self.assertDictEqual(counter, self.analyzer.get_piece_move_freq(pgn))
        
        with self.subTest():
            pgn = '1.e4 e5 2.Nf3 Nc6 3.d4 exd4 4.Bc4 h6 5.O-O Qe7 1-0'
            counter = Counter({'P':5, 'K':1,'N':2,'R':1,'B':1,'Q':1})

            self.assertDictEqual(counter, self.analyzer.get_piece_move_freq(pgn))

        
        
        


if __name__ == '__main__':
    unittest.main()