import React from "react";
import "../css/ListsInfo.css"



const number_of_matches = -1;
const offset = 0;
const BASE_URL = `http://localhost:8000`;
const url_get_info_all = BASE_URL + `/user/get_info_of_all_users`;
const url_get_matches_all = BASE_URL + `/matches/get_all_matches?number_of_matches=${number_of_matches}&offset=${offset}`;

export default class ListsInfo extends React.Component {
    constructor(props) {
        super(props);

        this.fetchData();

        this.state = {
            user_data_list: [],
            matches_list: [],
            status_response: "error"
        }

    }

    async fetchData() {
        try {
            const response = await fetch(url_get_info_all, {
                method: 'GET',
                credentials: 'include',
            });

            if (response.ok) {
                const data_res = await response.json();
                console.log(data_res);
                this.setState({ user_data_list: data_res.data, status_response: data_res.status });
            }


            const response1 = await fetch(url_get_matches_all, {
                method: 'GET',
                credentials: 'include',
            });

            if (response1.ok) {
                const data_res = await response1.json();
                console.log(data_res);
                this.setState({ matches_list: data_res.data, status_response: data_res.status });
            }
        } catch (error) {
            console.error('Произошла ошибка:', error);
        }
    }

    render() {
        return (
            <div className="game-statistics">
                <div className="matches_info">
                    <h3>Information of matches</h3>
                    <table className="table-statistics-info-m">
                        <thead>
                        <tr>
                            <th>ID</th>
                            <th>Game mode</th>
                            <th>Date of match</th>
                            <th>Match duration</th>
                            <th>First player</th>
                            <th>Second player</th>
                            <th>Rate change 1st player</th>
                            <th>Rate change 2nd player</th>
                        </tr>
                        </thead>
                        {this.getMatches()}
                    </table>
                </div>
                <div className="users_info">
                    <h3>Information of users</h3>
                    <table className="table-statistics-info-u">
                        <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nickname</th>
                            <th>Number matches Blitz</th>
                            <th>Number matches Rapid</th>
                            <th>Number matches Classical</th>
                            <th>Rate Blitz</th>
                            <th>Rate Rapid</th>
                            <th>Rate Classical</th>
                            <th>Winrate Blitz</th>
                            <th>Winrate Rapid</th>
                            <th>Winrate Classical</th>
                        </tr>
                        </thead>
                        {this.getUsers()}
                    </table>
                </div>

            </div>


        )
    }

    getUsers() {
        if (this.state.status_response !== "error" && this.state.user_data_list.length > 0) {
            console.log(this.state.user_data_list)
            return (
                <tbody className="list-users">
                {this.state.user_data_list.map((elem) => (
                    <tr key={elem.id}>
                        <td>{elem.id}</td>
                        <td>{elem.nickname}</td>
                        <td>{elem.number_matches_blitz}</td>
                        <td>{elem.number_matches_rapid}</td>
                        <td>{elem.number_matches_classical}</td>
                        <td>{elem.rate_blitz}</td>
                        <td>{elem.rate_rapid}</td>
                        <td>{elem.rate_classical}</td>
                        <td>{elem.winrate_blitz}</td>
                        <td>{elem.winrate_rapid}</td>
                        <td>{elem.winrate_classical}</td>
                    </tr>
                ))}
                </tbody>
            )
        } else {
            return (
                <div className="user">
                    <h3>No users</h3>
                </div>
            )
        }
    }
    getMatches() {
        if (this.state.status_response !== "error" && this.state.matches_list.length > 0) {
            console.log(this.state.matches_list)
            return (
                <tbody className="list-matches">
                {this.state.matches_list.map((elem) => (
                    <tr key={elem.id}>
                        <td>{elem.id}</td>
                        <td>{this.setMode(elem.mode_id)}</td>
                        <td>{this.setDate(elem.played_at)}</td>
                        <td>{this.setTime(elem.game_length_sec)}</td>
                        <td>{elem.player_1_nickname}</td>
                        <td>{elem.player_2_nickname}</td>
                        <td>{elem.rate_change_1}</td>
                        <td>{elem.rate_change_2}</td>
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

    setDate(date) {
        return date.substring(0, 10);
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
