import Piece from "./Piece";

export default class Rook extends Piece {
  constructor(player){
    super(player, (player === 1? "https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg" : "https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg"));
  }

  isMovePossible(src, dest){
    let mod = src % 9;
    let diff = 9 - mod;
    return (Math.abs(src - dest) % 9 === 0 || (dest >= (src - mod) && dest < (src + diff)));
  }
  
  getSrcToDestPath(src, dest){
    let path = [], pathStart, pathEnd, incrementBy;
    if(src > dest){
      pathStart = dest;
      pathEnd = src;
    }
    else{
        
      pathStart = src;
      pathEnd = dest;
    }
    if(Math.abs(src - dest) % 9 === 0){
      incrementBy = 9;
      pathStart += 9;
    }
    else{
      incrementBy = 1;
      pathStart += 1;
    }

    for(let i = pathStart; i < pathEnd; i+=incrementBy){
      path.push(i);
    }
    console.log(path);
    return path;
  }
}