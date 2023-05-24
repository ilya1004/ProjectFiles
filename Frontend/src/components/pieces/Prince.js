import Piece from "./Piece";

const old = "https://upload.wikimedia.org/wikipedia/commons/7/7d/Commoner_Transparent.svg"

export default class Prince extends Piece {
    constructor(player) {
        super(
            player, player === 1
                ? old
                : "https://upload.wikimedia.org/wikipedia/commons/4/49/CommonerB_Transparent.svg"
        );
    }

    getSrcToDestPath(src, dest) {
        return [];
    }

    isMovePossible(src, dest) {
        const [x1, y1] = this.convertToXY(src);
        const [x2, y2] = this.convertToXY(dest);
        let legality = Math.abs(x2 - x1) + Math.abs(y2 - y1) < 5;
        return (
            (src - 10 === dest ||
                src - 9 === dest ||
                src - 8 === dest ||
                src - 1 === dest ||
                src + 1 === dest ||
                src + 8 === dest ||
                src + 9 === dest ||
                src + 10 === dest ||
                src - 20 === dest ||
                src - 18 === dest ||
                src - 16 === dest ||
                src - 2 === dest ||
                src + 2 === dest ||
                src + 16 === dest ||
                src + 18 === dest ||
                src + 20 === dest) &&
            legality
        );
    }

    getSrcToDestPath(src, dest) {
        let path = [],
            pathStart,
            pathEnd,
            incrementBy;
        if (src > dest) {
            pathStart = dest;
            pathEnd = src;
        } else {
            pathStart = src;
            pathEnd = dest;
        }
        if (Math.abs(src - dest) % 9 === 0) {
            incrementBy = 9;
            pathStart += 9;
        } else if (Math.abs(src - dest) % 10 === 0) {
            incrementBy = 10;
            pathStart += 10;
        } else if (Math.abs(src - dest) % 8 === 0) {
            incrementBy = 8;
            pathStart += 8;
        } else {
            incrementBy = 1;
            pathStart += 1;
        }

        for (let i = pathStart; i < pathEnd; i += incrementBy) {
            path.push(i);
        }
        return path;
    }
}
