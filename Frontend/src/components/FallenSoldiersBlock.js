import React from 'react';
import "../components/Chess.css"
import Square from './Square';

export default class FallenSoldierBlock extends React.Component {

  renderSquare(square, i, squareShade) {
    return <Square 
    piece = {square} 
    style = {square.style}
    />
  }

  render() {
    return (
      <div>
      <div className="board-row">{this.props.whiteFallenSoldiers?.map((ws, index) =>
        this.renderSquare(ws, index)
        )}</div>
      <div className="board-row">{this.props.blackFallenSoldiers?.map((bs, index) =>
        this.renderSquare(bs, index)
        )}</div>
      </div>
      );
  }
}