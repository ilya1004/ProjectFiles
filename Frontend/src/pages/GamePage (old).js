import React from "react";
import Game from "../chess_online/Game";

class GamePage extends React.Component {
    constructor(props) {
        super(props);

        const urlParams = new URLSearchParams(window.location.search);
        const serializedProps = urlParams.get('props');

        const data_url = JSON.parse(decodeURIComponent(serializedProps));
        console.log(data_url)

        this.setState({curr_user_id: data_url.curr_user_id,
            opponent_id: data_url.opponent_id})

        const socket = data_url.websocket;

        this.state = {
            curr_user_id: 0,
            opponent_id: 0,
            // websocket: null
        }
        socket.onclose = () => {
            // Обработчик разрыва соединения
            console.log("Соединение закрыто, попытка переподключения...");
            setTimeout(() => {
                this.socket = new WebSocket(`ws://localhost:8000/wse/${this.state.curr_user_id}`);
            }, 3000);
        };

        socket.onmessage = (event) => {
            const message = event.data;
            const jsonData = JSON.parse(message);
            console.log("Received JSON data:", jsonData);
        };


    }




    render() {
        return (
            <Game opponent_id={this.state.opponent_id}
                  curr_user_id={this.state.curr_user_id}
                  websocket={this.state.websocket}/>
        )
    }
}

export default GamePage;
