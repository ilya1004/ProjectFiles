import React from "react";
import Move from './Move.js'

export default class Moves extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            list_moves: []
        }

        this.setState({list_moves: this.props.list_moves})
    }

    render() {
        console.log(this.state.list_moves)
        return (
            <tbody className="list-moves">
            {this.state.list_moves.map((elem) => (
                <tr key={elem.id}>
                    <td>{elem.id}</td>
                    <td>{elem.from_to}</td>
                </tr>
            ))}
            </tbody>

        )
    }

}