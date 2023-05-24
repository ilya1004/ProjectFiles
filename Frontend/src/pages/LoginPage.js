import { Card, Form, Button } from 'react-bootstrap';
import React from "react";
import "../css/Login.css"
import {Link, Route, Routes} from "react-router-dom";
import SignUp from "./SignUpPage";

const BASE_URL = `http://localhost:8000`
const url_login = BASE_URL + `/auth/jwt/login`

class Login extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            email: "",
            password: "",
            inputValue: "error"
        };
    }

    handleSubmit = (e) => {
        e.preventDefault();

        let data = new URLSearchParams();
        data.append('grant_type', '');
        data.append('username', this.state.email);
        data.append('password', this.state.password);
        data.append('scope', '');
        data.append('client_id', '');
        data.append('client_secret', '');

        fetch(url_login, {
            method: 'POST',
            credentials: 'include',
            body: new URLSearchParams(data)
        })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                this.setState({inputValue: data.status})
                if (data.status === "success") {
                    window.location.href = '/home';
                } else {
                    alert("User with given email is not registered")
                    this.setState({email: "", password: ""})
                }
                console.log(data);
            })
    };

    handleChange = (e) => {
        this.setState({ [e.target.name]: e.target.value });
    };

    render() {
        return (
            <div>
                <div className="login-form">
                    <Card className="card-form-l">
                        <Card.Body className="card-form">
                            <h1 className="text-center mb-4">Log In</h1>
                            <Form onSubmit={this.handleSubmit}>
                                <Form.Group className="group-form" id="email">
                                    <Form.Label className="labels-form">Email</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="email"
                                        value={this.state.email}
                                        onChange={this.handleChange}
                                        required
                                    />
                                </Form.Group>
                                <Form.Group className="group-form" id="password">
                                    <Form.Label className="labels-form">Password</Form.Label>
                                    <Form.Control
                                        type="password"
                                        name="password"
                                        value={this.state.password}
                                        onChange={this.handleChange}
                                        required
                                    />
                                </Form.Group>
                                <Button className="button-form" type="submit">
                                    Log In
                                </Button>
                            </Form>
                        </Card.Body>
                    </Card>
                    <div className="w-100 text-center mt-2">
                        Dont have an account?{" "}
                        <Link className="link-primary" to="/reg">Sign Up</Link>
                    </div>
                <Routes>
                    <Route path="/reg" element ={<SignUp/>} />
                </Routes>
                </div>
            </div>
        );
    }
}


export default Login;
