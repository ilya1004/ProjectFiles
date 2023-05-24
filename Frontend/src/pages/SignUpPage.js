import React from 'react';
import { Card, Form, Button } from 'react-bootstrap';
import {Link} from "react-router-dom";
import "../css/Login.css"

const BASE_URL = `http://localhost:8000`
const url_register = BASE_URL + `/auth/register`

class SignUp extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            nickname: "",
            email: "",
            password: "",
            passwordConfirm: ""
        };
    }


    handleSubmit = (e) => {
        e.preventDefault();

        if (this.state.password !== this.state.passwordConfirm) {
            alert("You are entered different passwords");
            this.setState({nickname: "", email: "", password: "", passwordConfirm: ""})
        } else {

            const data = {
                "email": this.state.email,
                "password": this.state.password,
                "is_active": true,
                "is_superuser": false,
                "is_verified": false,
                "nickname": this.state.nickname
            }

            console.log(data)

            fetch(url_register, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
                .then((response) => {
                    return response.json()
                })
                .then((data) => {
                    this.setState({inputValue: data.status})
                    if (data.email === this.state.email) {
                        window.location.href = '/';
                    }
                    console.log(data);
                })
        }
    };

    goToLogin() {
        window.location.href = '/';
    }

    handleChange = (e) => {
        this.setState({ [e.target.name]: e.target.value });
    };

    render() {
        return (
            <div>
                <div className="signup-form">
                    <Card className="card-form-s">
                        <Card.Body className="card-form">
                            <h2 className="text-center mb-4">Sign Up</h2>
                            <Form onSubmit={this.handleSubmit}>
                                <Form.Group className="group-form" id="nickname">
                                    <Form.Label className="labels-form">Nickname</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="nickname"
                                        value={this.state.nickname}
                                        onChange={this.handleChange}
                                        required
                                    />
                                </Form.Group>
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
                                <Form.Group className="group-form" id="password-confirm">
                                    <Form.Label className="labels-form">Password Confirmation</Form.Label>
                                    <Form.Control
                                        type="password"
                                        name="passwordConfirm"
                                        value={this.state.passwordConfirm}
                                        onChange={this.handleChange}
                                        required
                                    />
                                </Form.Group>
                                <Button className="button-form" type="submit">
                                    Sign Up
                                </Button>
                            </Form>
                        </Card.Body>
                    </Card>
                    <div className="w-100 text-center mt-2">
                        Already have an account?{" "}
                        <Link className="link-primary" to="/">Log In</Link>
                    </div>
                </div>
            </div>
        );
    }
}


export default SignUp;
