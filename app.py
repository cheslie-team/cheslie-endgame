from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Cheslie endgame API',
          description='Probe endgame databases',
          )

ns = api.namespace('v1', description='Cheslie endgame api')

endgameModel = api.model('EndgameDB', {
    'id': fields.String(readOnly=True, description='The endgame database unique identiier'),
    'name': fields.String(required=True, description='Name of the database'),
    'description': fields.String(required=True, description='Description')
})


class EndgameDAO(object):
    def __init__(self):
        self.endgames = []

    def get(self, id):
        for endgame in self.endgames:
            if endgame['id'] == id:
                return endgame
        api.abort(404, "Endgame {} doesn't exist".format(id))

    def create(self, data):
        endgame = data
        self.endgames.append(endgame)
        return endgame


DAO = EndgameDAO()
DAO.create({'id': 'syzygy',
            'name': 'Syzygy endgame database',
            'description': 'Syzygy tablebases provide WDL and DTZ information for all endgame positions with up to 6 pieces, allowing you to make progress, keeping a win in hand, winning all won positions, bringing all drawn positions over the fifty-move line.'})


@ns.route('/')
class EndgameList(Resource):
    @ns.doc('list_endgames')
    @ns.marshal_list_with(endgameModel)
    def get(self):
        return DAO.endgames


@ns.route('/<string:id>')
@ns.response(404, 'Endgame database not found')
@ns.param('id', 'The endgame database identifier')
class Endgame(Resource):
    @ns.doc('get_probe_results')
    @ns.marshal_with(endgameModel)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

if __name__ == '__main__':
    app.run(debug=True)
