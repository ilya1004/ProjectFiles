import Piece from "./Piece";

export default class King extends Piece {
  constructor(player) {
    super(
      player,
      player === 1
        ? "https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_klt45.svg"
        : "https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg"
    );
  }

  isMovePossible(src, dest) {
    return (
      src - 10 === dest ||
      src - 9 === dest ||
      src - 8 === dest ||
      src - 1 === dest ||
      src + 1 === dest ||
      src + 8 === dest ||
      src + 9 === dest ||
      src + 10 === dest 
      
    );
  }

    
  getSrcToDestPath(src, dest) {
    return [];
  }
}
