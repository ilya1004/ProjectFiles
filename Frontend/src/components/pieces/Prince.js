import Piece from "./Piece";

export default class Prince extends Piece {
  constructor(player) {
    super(
      player,
      player === 1
        ? "https://upload.wikimedia.org/wikipedia/commons/b/b0/%D0%A4%D0%B8%D0%B3%D1%83%D1%80%D0%B0_%D0%BA%D0%BD%D1%8F%D0%B6%D0%B8%D1%87%D0%B0_%D0%B2_%D0%B8%D0%B3%D1%80%D0%B5_%D0%91%D0%B5%D0%BB%D0%BE%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D1%88%D0%B0%D1%85%D0%BC%D0%B0%D1%82%D1%8B_%D0%B4%D0%BB%D1%8F_Windows.png"
        : "https://upload.wikimedia.org/wikipedia/commons/b/b0/%D0%A4%D0%B8%D0%B3%D1%83%D1%80%D0%B0_%D0%BA%D0%BD%D1%8F%D0%B6%D0%B8%D1%87%D0%B0_%D0%B2_%D0%B8%D0%B3%D1%80%D0%B5_%D0%91%D0%B5%D0%BB%D0%BE%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D1%88%D0%B0%D1%85%D0%BC%D0%B0%D1%82%D1%8B_%D0%B4%D0%BB%D1%8F_Windows.png"
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
      src + 10 === dest ||
      src - 20 === dest ||
      src - 18 === dest ||
      src - 16 === dest ||
      src - 2 === dest ||
      src + 2 === dest ||
      src + 16 === dest ||
      src + 18 === dest ||
      src + 20 === dest

    );
  }

  getSrcToDestPath(src, dest) {
    return [];
  }
}
