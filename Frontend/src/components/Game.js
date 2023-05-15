import React from "react";
import "../components/Chess.css";
import Board from "./Board.js";
import FallenSoldierBlock from "./FallenSoldiersBlock.js";
import initialiseChessBoard from "./InitializeChessBoard.js";
import classes from "./Game.module.css"

export default class Game extends React.Component {
  constructor() {
    super();
    this.state = {
      squares: initialiseChessBoard(),
      whiteFallenSoldiers: [],
      blackFallenSoldiers: [],
      player: 1,
      sourceSelection: -1,
      status: "",
      turn: "white",
    };
  }

  handleClick(i) {
    const squares = this.state.squares.slice();

    if (this.state.sourceSelection === -1) {
      if (!squares[i] || squares[i].player !== this.state.player) {
        this.setState({
          status:
            "Wrong selection. Choose player " + this.state.player + " pieces.",
        });
        if(squares[i])
        {
            squares[i].style = {...squares[i].style, backgroundColor:""};
            //console.log("First deletion is called");
            //delete squares[i].style.backgroundColor;
            //squares[i] = React.cloneElement(squares[i], {}, null);
            //squares[i].render
        }
        //squares[i] ? (delete squares[i].style.backgroundColor) : null;
      } else {
        squares[i].style = {
          ...squares[i].style,
          backgroundColor: "RGB(111,143,114)",
        }; 
        this.setState({
          status: "Choose destination for the selected piece",
          sourceSelection: i,
        });
      }
    } else if (this.state.sourceSelection > -1) {
        squares[this.state.sourceSelection].style = {...squares[this.state.sourceSelection].style, backgroundColor:""};
      //delete squares[this.state.sourceSelection].style.backgroundColor;
      //squares[this.state.sourceSelection] = React.cloneElement(squares[this.state.sourceSelection], {}, null);
      //console.log("Second deletion called");
      if (squares[i] && squares[i].player === this.state.player) {
        this.setState({
          status: "Wrong selection. Choose valid source and destination again.",
          sourceSelection: -1,
        });
      } else {
        const squares = this.state.squares.slice();
        const whiteFallenSoldiers = this.state.whiteFallenSoldiers.slice();
        const blackFallenSoldiers = this.state.blackFallenSoldiers.slice();
        const isDestEnemyOccupied = squares[i] ? true : false;
        const isMovePossible = squares[
          this.state.sourceSelection
        ].isMovePossible(this.state.sourceSelection, i, isDestEnemyOccupied);
        const srcToDestPath = squares[
          this.state.sourceSelection
        ].getSrcToDestPath(this.state.sourceSelection, i);
        const isMoveLegal = this.isMoveLegal(srcToDestPath);

        if (isMovePossible && isMoveLegal) {
          if (squares[i] !== null) {
            if (squares[i].player === 1) {
              whiteFallenSoldiers.push(squares[i]);
            } else {
              blackFallenSoldiers.push(squares[i]);
            }
          }
          console.log("whiteFallenSoldiers", whiteFallenSoldiers);
          console.log("blackFallenSoldiers", blackFallenSoldiers);
          squares[i] = squares[this.state.sourceSelection];
          squares[this.state.sourceSelection] = null;
          let player = this.state.player === 1 ? 2 : 1;
          let turn = this.state.turn === "white" ? "black" : "white";
          this.setState({
            sourceSelection: -1,
            squares: squares,
            whiteFallenSoldiers: whiteFallenSoldiers,
            blackFallenSoldiers: blackFallenSoldiers,
            player: player,
            status: "",
            turn: turn,
          });
        } else {
          this.setState({
            status:
              "Wrong selection. Choose valid source and destination again.",
            sourceSelection: -1,
          });
        }
      }
    }
  }

  
  isMoveLegal(srcToDestPath) {
    let isLegal = true;
    for (let i = 0; i < srcToDestPath.length; i++) {
      if (this.state.squares[srcToDestPath[i]] !== null) {
        isLegal = false;
      }
    }
    return isLegal;
  }

  render() {
    return (
      <div className={classes.gamepage}>
        <div className={classes.game}>
          <div className={classes.avanickrate}><div>ava</div><div>Nickname</div><div>Rate</div></div>
          <div className="fallen-soldier-block">
            <FallenSoldierBlock whiteFallenSoldiers={this.state.whiteFallenSoldiers} />
          </div>
          <div className="game-board">
            <Board
              squares={this.state.squares}
              onClick={(i) => this.handleClick(i)}
            />
          </div>
          <div className="fallen-soldier-block">
              {
                <FallenSoldierBlock
                  
                  blackFallenSoldiers={this.state.blackFallenSoldiers}
                />
              }
          </div>
          <div className={classes.avanickrate}><div>ava</div><div>Nickname</div><div>Rate</div></div>
        </div> 
        <div className={classes.game_info}>

          <h2>Current game info</h2>
          <div className={classes.turntimebox}>
            <div>
              <h3>Turn:</h3>
              <div
                id="player-turn-box"
                style={{ backgroundColor: this.state.turn }}
              ></div>
            </div>
            <div className="game-status">{this.state.status}</div>
            <div className={classes.timer}>Timer</div>
          </div>
          <div className={classes.tablewrapper}>
            <table className={classes.movetable}>
                <tr><th>Move number</th><th>White's turn</th><th>Black's turn</th></tr>
                <tr><td>1</td><td>e4</td><td>e5</td></tr>
                <tr><td>1</td><td>e4</td><td>e5</td></tr>
                <tr><td>1</td><td>e4</td><td>e5</td></tr>
                <tr><td>1</td><td>e4</td><td>e5</td></tr>
                <tr><td>1</td><td>e4</td><td>e5</td></tr>
                <tr><td>1</td><td>e4</td><td>e5</td></tr>
                <tr><td>1</td><td>e4</td><td>e5</td></tr>
            </table>   
          </div>
        </div>
        

        
      </div>
    );
  }
}


