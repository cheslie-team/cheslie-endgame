import unittest
import chess
from syzygy import Syzygy



class TestSyzygy(unittest.TestCase):

    def test_bestmove_black(self):
        syzygy = Syzygy()
        board = chess.Board('8/2K5/4B3/3N4/8/8/4k3/8 b - - 0 1')
        self.assertEqual(syzygy.probe(board)['bestMove'], 'e2d3')

    def test_bestmove_white(self):
        syzygy = Syzygy()
        board = chess.Board('8/2K5/4B3/3N4/8/8/4k3/8 w - - 0 1')
        self.assertEqual(syzygy.probe(board)['bestMove'], 'c7d6')

if __name__ == '__main__':
    unittest.main()