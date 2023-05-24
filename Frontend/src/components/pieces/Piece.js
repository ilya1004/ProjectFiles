

export default class Piece {
    constructor(player, iconUrl, str) {
        this.player = player;
        this.style = { backgroundImage: `url(` + iconUrl + `)` };
        this.str = str
    }
    convertToXY(ind){
        return [ind % 9, Math.floor(ind / 9)];
    };

}
