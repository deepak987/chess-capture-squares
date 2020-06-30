import re
import numpy as np
from matplotlib.colors import LogNorm
from collections import Counter
import pickle
import seaborn as sns
import matplotlib.pylab as plt


class OpeningAnalyzer:
    def __init__(self, data_file):
        self.game_dict_openings = data_file
    
    def get_piece_move_freq(self, game_string):
        """Find the number of times each piece was moved
        
        Parameters
        ----------
        game_string : string
            A string in the pgn format, from move 1 to the end of game
        
        Returns
        -------
        a counter object with the occurances of each piece. 
        Rook, knight, Bishop, Queen, King, Pawn represented as 
        R, N, B, Q, K, P resp.
        """
        moves = game_string.split()
        stripped_moves = [a.split('.')[-1] for a in moves][:-1]
        counter = Counter({'P':0, 'K':0,'N':0,'R':0,'B':0,'Q':0})
        for move in stripped_moves:
            if move[0] == 'O':
                counter['R']+=1
                counter['K']+=1
            
            elif move[0].isupper():
                counter[move[0]]+=1
            
            else:
                counter['P']+=1


        return counter
        



    def get_capture_squares(self, pgn_string):
        """Find all squares where a capture occured
        
        Parameters
        ----------
        pgn_string : string
            A string in the pgn format
        
        Returns
        -------
        List(str)
            Each string is a Square on the chessboard - (a1 - h8)
        """
        
        regex_captures = '([A-Za-z]+x[a-h][1-8])'
        all_captures = re.findall(regex_captures, pgn_string)
        capture_squares = [s.split('x')[-1] for s in all_captures]
        return capture_squares

    def counter_to_array(self, ctr):
        """Create a chessboard from a counter
        
        Parameters
        ----------
        ctr : Collections.counter object

        Returns
        -------
        np.array((8x8))
        """
        
        ranks = ['a','b','c','d','e','f','g','h']
        chessboard = np.zeros((8,8))
        all_squares = []
        for i in range(8,0,-1):
            for rank in ranks:
                all_squares.append(rank+str(i))
        count = 0
        for i in range(chessboard.shape[0]):
            for j in range(chessboard.shape[1]):
                chessboard[i][j] = ctr[all_squares[count]]
                count+=1
        return chessboard


    def get_piece_move_opening(self, ECO_code_list):
        """Get the frequency of piece moves by opening
        
        Parameters
        ----------
        ECO_code_list : list(str)
            list of ECO codes
        
        Returns
        -------
        Counter
        """

        counter = self.get_piece_move_freq('')
        for opening in ECO_code_list:
            opening_pgns = self.game_dict_openings[opening]
            for pgn in opening_pgns:
                game_string = pgn['Game']
                counter = counter + self.get_piece_move_freq(game_string)
        return counter

    def create_capture_board(self, ECO_code_list, plot = False):
        """Create a numpy array with number of captures per square
           from all games having input ECO codes
        
        Parameters
        ----------
        ECO_code_list : List[str]
            
        Returns
        -------
        2d numpy array
        """
        BATCH_SIZE = 300000
        
        chessboard = np.zeros((8,8))
        for code in ECO_code_list:
            game_list = self.game_dict_openings[code]
            previously_processed = 0
            while previously_processed < len(game_list):
                batch = [g['Game'] for g in game_list[previously_processed:previously_processed+BATCH_SIZE]]
                previously_processed += BATCH_SIZE
                
            
                game_move_string = ' '.join(batch)
                all_capture_squares = self.get_capture_squares(game_move_string)
                ctr = Counter(all_capture_squares)
                chessboard = chessboard + self.counter_to_array(ctr)
        if plot:
            self.plot_chessboard(chessboard)
        return chessboard
    
    def plot_chessboard(self, board):
        """plot the log-normal frequency of the board
        
        Parameters
        ----------
        board : 8x8 array
        """
        if board.min() == 0:
            board = board+1 # log normal plot
        ylabels = [i for i in range(8,0,-1)]
        xlabels = ['a','b','c','d','e','f','g','h']
        ax = sns.heatmap(board, linewidth=0.1, cmap="Greens", xticklabels=xlabels, yticklabels=ylabels, norm=LogNorm(board.min(),board.max()))
        plt.show()

if __name__ == "__main__":
    with open('all_processed_data.pkl', 'rb') as handle:
        game_dict_openings = pickle.load(handle)
        analyzer = OpeningAnalyzer(game_dict_openings)
    
    print(analyzer.get_piece_move_opening(['A00']))
        
    


