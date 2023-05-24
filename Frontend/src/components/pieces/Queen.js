import Piece from "./Piece";

export default class Queen extends Piece {
    constructor(player){
      super(player, (player === 1? "https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg" : "https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg"));
    }
  
    isMovePossible(src, dest){
      let mod = src % 8;
      let diff = 8 - mod;
      const [x1, y1] = this.convertToXY(src);
      const [x2, y2] = this.convertToXY(dest);
      console.log(x1, y1);
      console.log(x2, y2);
      console.log(src);
      console.log(dest);
      if(x1 != x2 && y1 != y2)
      {
        const [x1, y1] = this.convertToXY(src);
        const [x2, y2] = this.convertToXY(dest);
        let legality = Math.abs(x2 - x1) == Math.abs(y2 - y1);
        if(!legality)
          return false;
      }
      return (Math.abs(src - dest) % 10 === 0 || Math.abs(src - dest) % 8 === 0) ||
        (Math.abs(src - dest) % 9 === 0 || (dest >= (src - mod) && dest < (src + diff)));
    }

    getSrcToDestPath(src, dest){
      const [x1, y1] = this.convertToXY(src);
      const [x2, y2] = this.convertToXY(dest);
      let legality = Math.abs(x2 - x1) == Math.abs(y2 - y1);
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
      else if(Math.abs(src - dest) % 10 === 0 && legality){
        incrementBy = 10;
        pathStart += 10;
      }
      else if(Math.abs(src - dest) % 8 === 0 && legality){
        incrementBy = 8;
        pathStart += 8;
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