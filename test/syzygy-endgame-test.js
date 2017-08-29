var should = require('chai').should(),
    Chess = require('chess.js').Chess,
    Syzygy = require('./../modules/syzygy-endgame.js');

describe('When the endgame is initilized', function () {
    var endgame =Syzygy.Endgame;

    it('should not die'),

    describe('and a bestMove is called with a legal fen', function () {
        var chess = new Chess("8/2K5/4B3/3N4/8/8/4k3/8 b - - 0 1");

        it('should return a legal move', function () {
            endgame.bestMove(chess.fen()).should.be.oneOf(chess.moves());
        })
    });
});