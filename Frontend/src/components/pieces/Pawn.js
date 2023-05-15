import Piece from "./Piece";

export default class Pawn extends Piece {
  constructor(player) {
    super(
      player,
      player === 1
        ? "https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg"
        : "https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg"
    );
    this.initialPositions = {
      //1: [48, 49, 50, 51, 52, 53, 54, 55],
      1: [72, 71, 10, 69, 68, 67, 66, 65, 64],
      2: [9, 10, 11, 12, 13, 14, 15, 16, 17],
    };
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
