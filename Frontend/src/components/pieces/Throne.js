import Piece from "./Piece";

export default class Throne extends Piece{
  constructor() {
    super(0, "https://w7.pngwing.com/pngs/893/135/png-transparent-geometry-motif-geometric-shapes-symmetry-monochrome-sphere-thumbnail.png")
    this.initialPosition =  40;
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
    return false;
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
