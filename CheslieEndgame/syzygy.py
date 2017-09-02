import chess
import chess.syzygy


class Syzygy():
    def __init__(self):
        self.board = chess.Board()
        print('Loading syzygy tablebases ...')
        self.syzygy = chess.syzygy.Tablebases()

        path = 'CheslieEndgame/databases/syzygy/four-men'
        num = self.syzygy.open_directory(path)
        print('* Loaded %d syzygy tablebases from %r' % (num, path))

    def get_dtz_move(self, board, move):
        board.push(move)
        dtz_move = {'move': move.uci(),'dtz':self.syzygy.get_dtz(board)}
        board.pop()
        return dtz_move

    def probe(self, board):
        result = {}

        result['wdl'] = self.syzygy.get_wdl(board)
        result['dtz'] = self.syzygy.get_dtz(board)
        result['moves'] = [self.get_dtz_move(board,move) for move in board.legal_moves]
        
        if result['wdl'] == None:
            return None

        best_moves = []
        if result['wdl'] == 0:
            best_moves = [dtzMove for dtzMove in  result['moves'] if dtzMove['dtz']==0]
        if result['wdl'] > 0:
            best_moves = [dtzMove for dtzMove in  result['moves'] if dtzMove['dtz'] < 0]
        if result['wdl'] < 0:
            best_moves = [dtzMove for dtzMove in  result['moves'] if dtzMove['dtz'] > 0]

        result['bestMove'] = max(best_moves,key=lambda dtz_move: dtz_move['dtz'])['move']
        return result 
        