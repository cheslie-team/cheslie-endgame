from flask import Flask
from flask_restplus import Api, Resource, fields
from syzygy import Syzygy
import chess

app = Flask(__name__)
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
        board = chess.Board(fen)
        return self.syzygy.probe(board)
        # api.abort(404, "Endgame {} doesn't exist".format(id))


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


if __name__ == '__main__':
    app.run(debug=True)
