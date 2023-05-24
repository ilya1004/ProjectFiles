import React from "react";
import { Button } from "react-bootstrap";
import "../css/index.css"
import "../css/SelectMode.css"

const BASE_URL = `http://localhost:8000`
const url_get_info = BASE_URL + `/user/get_info_of_current_user`;
let socket;

class SelectModePage extends React.Component {
    constructor(props) {
        super(props);

        this.fetchData();

        this.state = {
            user_data: {},
            user_id: -1,
            matches_list: [],
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
                this.setState({ user_data: data_res.data, user_id: data_res.data.id });
            } else {
                console.error('Ошибка');
            }
        } catch (error) {
            console.error('Произошла ошибка:', error);
        }
    }

    componentDidMount() {
        this.fetchData();
    }

    render() {
        return (
            <div className="table-container">
                <table className="table-main">
                    <thead>
                    <tr>
                        <th>
                            <h1>Ranked</h1>
                        </th>
                        <th>
                            <h1>Unranked</h1>
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td className="td-sm">
                            <div className="buttons-container">
                                <Button onClick={() => this.handleModeSelect(1)}>
                                    Blitz (3 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(2)}>
                                    Blitz (5 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(3)}>
                                    Blitz (7 min)
                                </Button>
                            </div>
                        </td>
                        <td className="td-sm">
                            <div className="buttons-container">
                                <Button onClick={() => this.handleModeSelect(11)}>
                                    Blitz (3 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(12)}>
                                    Blitz (5 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(13)}>
                                    Blitz (7 min)
                                </Button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td className="td-sm">
                            <div className="buttons-container">
                                <Button onClick={() => this.handleModeSelect(4)}>
                                    Rapid (10 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(5)}>
                                    Rapid (13 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(6)}>
                                    Rapid (15 min)
                                </Button>
                            </div>
                        </td>
                        <td className="td-sm">
                            <div className="buttons-container">
                                <Button onClick={() => this.handleModeSelect(14)}>
                                    Rapid (10 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(15)}>
                                    Rapid (13 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(16)}>
                                    Rapid (15 min)
                                </Button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td className="td-sm">
                            <div className="buttons-container">
                                <Button onClick={() => this.handleModeSelect(7)}>
                                    Classical (20 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(8)}>
                                    Classical (30 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(9)}>
                                    Classical (60 min)
                                </Button>
                            </div>
                        </td>
                        <td className="td-sm">
                            <div className="buttons-container">
                                <Button onClick={() => this.handleModeSelect(17)}>
                                    Classical (20 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(18)}>
                                    Classical (30 min)
                                </Button>
                                <Button onClick={() => this.handleModeSelect(19)}>
                                    Classical (60 min)
                                </Button>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        );
    }

    handleModeSelect = (mode_id) => {

        // if (mode_id === 1) {
        //     const authToken = this.getAuthTokenFromCookie('cookie');
        //     console.log(authToken)
        // }



        socket = new WebSocket(`ws://localhost:8000/wse/${mode_id}/${this.state.user_id}`)
        socket.keepAlive = true;
        socket.onopen = () => {
            console.log("WebSocket connection established");
        };

        socket.onmessage = (event) => {
            const message = event.data;
            const jsonData = JSON.parse(message);
            console.log("Received JSON data:", jsonData);
            // if (jsonData.status === "success" && jsonData.data.substring(0, 16) === "Game has founded") {
                const props = { curr_user_id: this.state.user_id,
                    opponent_id: jsonData["details"], websocket: socket};
                const serializedProps = encodeURIComponent(JSON.stringify(props));
                window.location.href = `/game?props=${serializedProps}`;
            // }
        };

        socket.onclose = () => {
            console.log("Соединение закрыто, попытка переподключения...");
            setTimeout(() => {
                socket = new WebSocket(`ws://localhost:8000/wse/${mode_id}/${this.state.user_id}`);
                socket.keepAlive = true
            }, 1000);
        };

        // const url = "ws://localhost:8000/ws/1/1";
        // const url1 = `http://localhost:8000`;
        // socket = io(url1);


        // socket.onopen = () => {
        //     const authToken = this.getAuthTokenFromCookie('cookie');
        //     socket.send(JSON.stringify({ type: 'auth', token: authToken }));
        // };
    };

    getAuthTokenFromCookie(cookieName) {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(`${cookieName}`)) {
                return cookie.substring(cookieName.length + 1);
            }
        }
        return null;
    }


}

export default SelectModePage;

