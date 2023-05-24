import React from "react";
import "../css/Profile.css"

const number_of_matches = -1;
const offset = 0;
const BASE_URL = `http://localhost:8000`;
const url_get_matches = BASE_URL + `/matches/get_matches_of_current_user`;

class Matches extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            list_matches: [],
            status_response: "error"
        }

        this.fetchMatches();

    }

    async fetchMatches() {
        try {
            const response = await fetch(url_get_matches + `?number_of_matches=${number_of_matches}&offset=${offset}`, {
                method: 'GET',
                credentials: 'include',
            });

            if (response.ok) {
                const data_res = await response.json();
                this.setState({ status_response: data_res.status });
                console.log(typeof data_res.data)
                this.setState({ list_matches: data_res.data });
            }
        } catch (error) {
            console.error('Произошла ошибка:', error);
        }
    }

    render() {
        console.log(this.state.status_response)
        if (this.state.status_response !== "error") {
            return (
                <tbody className="list-matches">
                    {this.state.list_matches.map((elem) => (
                        <tr key={elem.id}>
                            <td>{this.setResMatch(elem.player_1_id, this.props.curr_user_id)}</td>
                            <td>{this.setMode(elem.mode_id)}</td>
                            <td>{this.setTime(elem.game_length_sec)}</td>
                            <td>{this.setOpponent(elem, this.props.curr_user_id)}</td>
                            <td>{this.setRateChange(elem, this.props.curr_user_id)}</td>
                        </tr>
                    ))}
                </tbody>

            )
        } else {
            return (
                <div className="match">
                    <h3>No matches</h3>
                </div>
            )
        }
    }

    setRateChange(elem, curr_user_id) {
        if (elem.player_1_id === curr_user_id) {
            return elem.rate_change_player_1;
        } else {
            return elem.rate_change_player_2;
        }
    }

    setOpponent(elem, curr_user_id) {
        if (elem.player_1_id === curr_user_id) {
            return elem.player_2_nickname;
        } else {
            return elem.player_1_nickname;
        }
    }

    setResMatch(player_winner_id, curr_user_id) {

        console.log("curr_user_id = " + curr_user_id)
        console.log("player_winner_id = " + player_winner_id)
        if (curr_user_id === player_winner_id) {
            return "Won match";
        } else {
            return "Lost match"
        }
    }

    setMode(mode_id) {
        if (mode_id === 0 || mode_id === 1 || mode_id === 2) {
            return "Blitz";
        } else if (mode_id === 3 || mode_id === 4 || mode_id === 5) {
            return "Rapid";
        } else if (mode_id === 6 || mode_id === 7 || mode_id === 8) {
            return "Classical";
        }
    }

    setTime(game_length) {
        let min = Math.floor(game_length / 60);
        let sec = game_length % 60;

        // console.log("game_length = " + game_length.toString()
        if (min > 0) {
            return `${min} minutes, ${sec} seconds`;
        } else if (min === 1) {
            return `${min} minute, ${sec} seconds`;
        } else {
            return `${sec} seconds`;
        }
    }
}

export default Matches;