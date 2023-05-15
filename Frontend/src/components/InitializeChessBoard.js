import Bishop from './pieces/Bishop.js';
import King from './pieces/King.js';
import Knight from './pieces/Knight.js';
import Pawn from './pieces/Pawn.js';
import Prince from './pieces/Prince.js';
import Queen from './pieces/Queen.js';
import Rook from './pieces/Rook.js';
import Throne from './pieces/Throne.js';

export default function initialiseChessBoard(){
  const squares = Array(81).fill(null);

  let YourSide = 1; //The player at bottom side of the board

  for(let i = 9; i < 18; i++){
    squares[i] = new Pawn(3-YourSide);
    squares[i+54] = new Pawn(YourSide);
  }
  squares[0] = new Rook(3-YourSide);
  squares[8] = new Rook(3-YourSide);
  squares[72] = new Rook(YourSide);
  squares[80] = new Rook(YourSide);

  squares[1] = new Knight(3-YourSide);
  squares[7] = new Knight(3-YourSide);
  squares[73] = new Knight(YourSide);
  squares[79] = new Knight(YourSide);

  squares[2] = new Bishop(3-YourSide);
  squares[6] = new Bishop(3-YourSide);
  squares[74] = new Bishop(YourSide);
  squares[78] = new Bishop(YourSide);

  squares[3] = new Queen(3-YourSide);
  squares[4] = new King(3-YourSide);
  squares[5] = new Prince(3-YourSide);

  squares[77] = new Queen(YourSide);
  squares[76] = new King(YourSide);
  squares[75] = new Prince(YourSide);

  squares[40] = new Throne();

  return squares;
}