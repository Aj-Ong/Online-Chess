import { useEffect, useState } from 'react';
import Chessboard from 'chessboardjsx';
import { socket } from './App.js';

function Square() {
  const [board, updateBoard] = useState([]);
  
  function fetch(){
    socket.emit('fetchboard');
    console.log("ran!");
  }

  function drag(square){
    console.log(square);
  }
  
  function drop(square){
    console.log("From "+ square.sourceSquare + " To: " + square.targetSquare + " Peice: " + square.piece);
    socket.emit('move', { 'moveTo': square.sourceSquare + square.targetSquare })
  }

  function mouseOut(square){
    console.log("MOUSE OUT " + square);
  }

  function mouseOver(square){
    console.log("MOUSE ON " + square);
  }

  function pieceClick(square){
    console.log(square);
  }

  useEffect(() => {
    socket.on('fetchboard', (data) => {
      console.log(data.board);
      let temp = data.board;
      console.log(typeof(temp))
      updateBoard(data.board);
    });
  }, [board]);

    return (
      <div >
        <button onClick={fetch}>FetchBoard</button>
        <Chessboard 
        position={board} 
        onDragOverSquare={drag}
        onDrop={drop}
        onMouseOutSquare={mouseOut}
        onMouseOverSquare={mouseOver}
        onPieceClick={pieceClick}
        />
      </div>
    );
  }
  
  export default Square;
  