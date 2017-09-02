from flask import Flask
from flask_restplus import Api, Resource, fields
import chess

from syzygy import Syzygy
from CheslieEndgame import app

api = Api(app, version='1.0', title='Cheslie endgame API',
          description='Probe endgame databases',)

ns = api.namespace('v1', description='Cheslie endgame api')

probeModel = api.model('EndgameDB', {
    'bestMove': fields.String(readOnly=True, description='The endgame database unique identiier'),
    'wdl': fields.String(readOnly=True, description='The endgame database unique identiier'),
    'dtz': fields.String(readOnly=True, description='The endgame database unique identiier')
})

parser = api.parser()
parser.add_argument('fen', type=str, required=True,
                    help='A Fen representing the board')


class probeDAO(object):
    def __init__(self):
        self.syzygy = Syzygy()

    def get(self, fen):
        try:
            board = chess.Board(fen)
        except ValueError:
            api.abort(404, "Illegal fen:  {}".format(fen))

        best_move =  self.syzygy.probe(board)
        if best_move is None:
            api.abort(404, "Board with fen, {}, not found in database".format(fen))
        return best_move


DAO = probeDAO()

@ns.route('/syzygy')
@ns.response(404, 'Endgame database not found')
@ns.param('fen', 'The fen representing the board')
class Endgame(Resource):
    @ns.doc('get_probe_results')
    @ns.marshal_with(probeModel)
    def get(self):
        '''Fetch a given resource'''
        args = parser.parse_args()
        return DAO.get(args.fen)



def wsgi_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    response_body = 'Hello World'
    yield response_body.encode()


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)