'use strict'
var Chess = require('chess.js').Chess,
    python = require('python'),
    sluk = function (err, data) { };

var Syzygy = class Syzygy {
    constructor() {
        this.shell = python.shell;
        this.fen;
        this.shell("import chess.syzygy", sluk);
        this.shell('table = chess.syzygy.open_tablebases("/home/shg/depot/others/tb/src/syzygy")', sluk);
    }

    probeDTZMove(board, move) {
        return new Promise(resolve => {
            board.move(move);
            this.shell('board = chess.Board("' + board.fen() + '")', sluk);
            this.shell('table.probe_dtz(board)', function (err, dtz) {
                resolve({
                    move: move,
                    dtz: parseInt(dtz)
                });
            });
        });
    }

    probeDTZ(board) {
        return new Promise(resolve => {
            this.shell('board = chess.Board("' + board.fen() + '")', sluk);
            this.shell('table.probe_dtz(board)', function (err, dtz) {
                resolve(dtz);
            });
        });
    }


    movesDtz(board) {
        var moves = board.moves().map((move) => {
            return (this.probeDTZMove(new Chess(board.fen()), move))
        });
        return Promise.all(moves);
    }


    bestMove(fen) {
        var chess = new Chess(fen);
        return new Promise(resolve => {
            this.movesDtz(chess).then(function (dtzMoves) {
                var bestMove;
                if (chess.turn() == 'b') {
                    dtzMoves = dtzMoves.map((move) => {
                        move.dtz = move.dtz * -1;
                        return move
                    })
                };
                if (dtzMoves.some((dtzMove) => { return dtzMove.dtz < 0 })) {
                    dtzMoves = dtzMoves.filter((dtzMove) => { return dtzMove.dtz < 0 });
                    bestMove = dtzMoves.sort((a, b) => {return a.dtz - b.dtz }).pop().move;
                } else if (dtzMoves.some((dtzMove) => { return dtzMove.dtz == 0 })) {
                    bestMove = dtzMoves.find((dtzMove) => {return dtzMove.dtz == 0 })[0].move;
                } else {
                    dtzMoves = dtzMoves.filter((dtzMove) => { return dtzMove.dtz > 0 });                    
                    bestMove = dtzMoves.sort((a, b) => { return b.dtz - a.dtz })[0].move;
                }
                resolve(bestMove);
            })
        })
    };
};



module.exports.Endgame = Syzygy;