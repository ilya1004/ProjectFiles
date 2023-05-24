import Piece from "./Piece";

export default class Throne extends Piece{
  constructor() {
      super(3, "https://upload.wikimedia.org/wikipedia/commons/2/20/Chess_Mlt45.svg")
    this.initialPosition =  40;
    this.player = 3;
  }

  isMovePossible(src, dest, isDestEnemyOccupied) {
      if (this.player === 1) {
          if (
              (dest === src - 9 && !isDestEnemyOccupied) ||
              (dest === src - 18 && this.initialPositions[1].indexOf(src) !== -1)
          ) {
              return true;
          } else if (
              isDestEnemyOccupied &&
              (dest === src - 10 || dest === src - 8)
          ) {
              return true;
          }
      } else if (this.player === 2) {
          if (
              (dest === src + 9 && !isDestEnemyOccupied) ||
              (dest === src + 18 && this.initialPositions[2].indexOf(src) !== -1)
          ) {
              return true;
          } else if (
              isDestEnemyOccupied &&
              (dest === src + 10 || dest === src + 8)
          ) {
              return true;
          }
      }
  }

    getSrcToDestPath(src, dest) {
        if (dest === src - 18) {
            return [src - 9];
        } else if (dest === src + 18) {
            return [src + 9];
        }
        return [];
    }
}
