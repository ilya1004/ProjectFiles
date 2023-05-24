import Piece from "./Piece";

export default class Knight extends Piece {
  constructor(player){
    super(player, (player === 1? "https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg" : "https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg"));
  }

  isMovePossible(src, dest){
    const [x1, y1] = this.convertToXY(src);
    const [x2, y2] = this.convertToXY(dest);
    let legality = Math.abs(x2 - x1) + Math.abs(y2 - y1) < 4; 

    return (src - 19 === dest || 
      src - 11 === dest || 
      src + 7 === dest || 
      src + 17 === dest || 
      src - 17 === dest || 
      src - 7 === dest || 
      src + 11 === dest || 
      src + 19 === dest) &&
      legality;
  }

  /**
   * always returns empty array because of jumping
   * @return {[]}
   */
  getSrcToDestPath(){
    return [];
  }
}