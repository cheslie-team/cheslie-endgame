var should = require('chai').should(),
    Chess = require('chess.js').Chess,
    Syzygy = require('./../modules/syzygy-endgame.js');

describe('When the endgame is initilized', function () {
    var endgame =new Syzygy.Endgame();

    it('should not die'),

    describe('and a bestMove is called with a legal fen', function () {
        var chess;
        beforeEach('The game is created', () => {
            chess = new Chess("8/2K5/4B3/3N4/8/8/4k3/8 b - - 0 1");
        });
        

        it('should return a legal move', function () {
            endgame.bestMove(chess.fen()).then(function(move) {move.should.be.oneOf(chess.moves())});
        })

        it('should return blacks best move ', function (done) {     
            endgame.bestMove(chess.fen()).then(function(move) {
                move.should.equal("Kd3");
                    done();
            });
        })

        it('should return whites best move ', function (done) { 
            chess.move('Kd3');    
            endgame.bestMove(chess.fen()).then(function(move) {
                move.should.be.oneOf(['Bf5+','Kd6']);
                done();
            });
        })
    });
});