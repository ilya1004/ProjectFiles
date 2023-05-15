import React, { useState, useEffect } from "react";
import Game from "../components/Game";

function PlayPage() {
    return (<Game/>);
  //return <div>Here will be a game</div>;

  /*const [chess, setChess] = useState([]);

  const black = {
    width: "10vh",
    height: "10vh",
    backgroundColor: "black",
    flexWrap: "wrap",
  };

  const white = {
    width: "10vh",
    height: "10vh",
    backgroundColor: "white",
    flexWrap: "wrap",
  };

  const chessBox = {
    width: "90vh",
    height: "90vh",
    display: "flex",
    flexWrap: "wrap",
  };

  const makeChessBoard = () => {
    let arr = [];
    for (let i = 0; i < 9; i++) {
      let temp = [];
      for (let j = 0; j < 9; j++)
        if ((i + j) % 2) temp.push(<div style={white}></div>);
        else temp.push(<div style={black}></div>);
      arr.push(temp);
    }
    setChess(arr);
  };

  useEffect(() => {
    makeChessBoard();
  });

  return (
    <div>
      <section style={chessBox}>{chess}</section>
    </div>
  );*/
}

export default PlayPage;
