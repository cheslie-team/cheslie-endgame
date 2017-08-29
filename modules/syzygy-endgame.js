'use strict'
var Chess = require('chess.js').Chess,
    bestMove = function (fen) {
        var chess = new Chess(fen);
        var moves = chess.moves()
        return moves[1];
    };

module.exports.Endgame = { bestMove: bestMove };