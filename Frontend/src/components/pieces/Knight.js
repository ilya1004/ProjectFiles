import Piece from "./Piece";

export default class Knight extends Piece {
  constructor(player){
    super(player, (player === 1? "https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg" : "https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg"));
  }

  isMovePossible(src, dest){
    return (src - 19 === dest || 
      src - 11 === dest || 
      src + 7 === dest || 
      src + 17 === dest || 
      src - 17 === dest || 
      src - 7 === dest || 
      src + 11 === dest || 
      src + 19 === dest);
  }

  /**
   * always returns empty array because of jumping
   * @return {[]}
   */
  getSrcToDestPath(){
    return [];
  }
}