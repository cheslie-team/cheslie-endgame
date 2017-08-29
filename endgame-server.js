var config = require('cheslie-config'),
server = require('http').createServer(),
io = require('socket.io').listen(server),
endgame = require('./modules/syzygy-endgame.js').Endgame;

io.on('connect', function (socket) {
socket.on('join', function (gameId, playerName) {
  
})

socket.on('move', function (board) {
  return endgame.bestMove(board)
});

socket.on('disconnect', function () {
});
});

server.listen(2207, function () {
console.log('Running server on port: ' + 2207)
});