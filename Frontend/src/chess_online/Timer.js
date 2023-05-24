import React from 'react';

class Timer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            seconds: 0
        };
    }

    componentDidMount() {
        this.timerID = setInterval(() => {
            this.setState((prevState) => ({
                seconds: prevState.seconds + 1
            }));
        }, 1000);
    }

    componentWillUnmount() {
        clearInterval(this.timerID);
    }

    render() {
        const { seconds } = this.state;
        return (
            <div>
                <h3>{10} seconds</h3>
            </div>
        );
    }
}

export default Timer;
