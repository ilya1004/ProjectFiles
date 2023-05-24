import { Button } from "react-bootstrap";
import React from "react";
import Matches from "../components/Matches";
import "../css/Profile.css"
import ChangeNickname from "../services/ChangeNickname";
import Avatar from "../img/zahar.jpg"
import WarningModal from "../components/WarningModal";

const BASE_URL = `http://localhost:8000`
const url_get_info = BASE_URL + `/user/get_info_of_current_user`;
const url_logout = BASE_URL + `/auth/jwt/logout`;

class Profile extends React.Component {
    constructor(props) {
        super(props);

        this.fetchData();

        this.state = {
            user_data: {},
            matches_list: [],
            status_response: "error"
        }

    }

    async fetchData() {
        try {
            const response = await fetch(url_get_info, {
                method: 'GET',
                credentials: 'include',
            });

            if (response.ok) {
                const data_res = await response.json();
                console.log(data_res);
                this.setState({ user_data: data_res.data, status_response: data_res.status });
            }
        } catch (error) {
            console.error('Произошла ошибка:', error);
        }
    }

    componentDidMount() {
        this.fetchData();
    }

    render() {
        if (this.state.status_response === "success") {
            return (
                <div className="prof-page">
                    <div className="personal-data">
                        <div className="visual-information">
                            <div className="profile-avatar">
                                <img className="profile-avatar-img" src={Avatar} alt="Error"/>
                            </div>
                            <div className="stat-boxes">
                                <ul className="stats">
                                    <h5>Nickname</h5>
                                    <li>{this.state.user_data.nickname}</li>
                                    <h5>Overall match number</h5>
                                    <li>{this.state.user_data.number_matches_blitz + this.state.user_data.number_matches_rapid
                                        + this.state.user_data.number_matches_classical}</li>
                                    <h5>Average rate</h5>
                                    <li>{Math.round((this.state.user_data.rate_blitz + this.state.user_data.rate_rapid +
                                        this.state.user_data.rate_classical) / 3.0)}</li>
                                </ul>
                            </div>
                        </div>
                        <br/>
                        <div className="settings-buttons-block">
                            <ChangeNickname/>
                            <div>
                                <Button className="setting-button" onClick={this.quitTheProfile}>Quit the
                                    account</Button>
                            </div>
                        </div>
                    </div>
                    <div className="game-statistics">
                        <h3>My statistics</h3>
                        <table className="table-statistics">
                            <thead>
                            <tr>
                                <th>Number of games</th>
                                <th>Rate</th>
                                <th>Winrate</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr>
                                <td>{this.state.user_data.number_matches_blitz}</td>
                                <td>{this.state.user_data.rate_blitz}</td>
                                <td>{this.state.user_data.winrate_blitz}</td>
                            </tr>
                            <tr>
                                <td>{this.state.user_data.number_matches_rapid}</td>
                                <td>{this.state.user_data.rate_rapid}</td>
                                <td>{this.state.user_data.winrate_rapid}</td>
                            </tr>
                            <tr>
                                <td>{this.state.user_data.number_matches_classical}</td>
                                <td>{this.state.user_data.rate_classical}</td>
                                <td>{this.state.user_data.winrate_classical}</td>
                            </tr>
                            </tbody>
                        </table>
                        <br/>
                        <h3 className="stat-header">Match history</h3>
                        <table className="table-statistics">
                            <thead>
                            <tr>
                                <th>Result</th>
                                <th>Game mode</th>
                                <th>Match duration</th>
                                <th>Opponent</th>
                                <th>Rate change</th>
                            </tr>
                            </thead>
                            <Matches curr_user_id={this.state.user_data.id}/>
                        </table>
                    </div>
                </div>
            )
        } else {
            return (
                <div>
                <WarningModal/>
            </div>
            )
        }
    }


    changeNickname() {
        fetch('/change_curr_user_nickname', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ new_nickname: 'Новый никнейм' })
        })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                console.log(data);
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });

    }

    quitTheProfile() {

        fetch(url_logout, {
            method: 'POST',
            credentials: 'include',
        })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                console.log(data);
            })

        window.location.href = '/';
    }
}


export default Profile;
