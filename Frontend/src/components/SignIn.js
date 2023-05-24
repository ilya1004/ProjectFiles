import React, { Fragment, useRef } from "react";
import { Form, Button, Card } from "react-bootstrap";
import { useDispatch } from "react-redux";
import { login } from "../features/user";

function SignIn() {
    const dispatch = useDispatch()

  const emailRef = useRef();
  const passwordRef = useRef();

  function handleSubmit(e) {
    e.preventDefault();
    dispatch(login({name: "defname", rate: 1}));
    console.log("Sign in handler called");
  }
  return (
    <>
      <div className="justify-content-center d-flex mt-5">
        <Card>
          <Card.Body>
            <h2 className="text-center mb-4">Sign In</h2>
            <Form onSubmit={handleSubmit}>
              
              <Form.Group id="email">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" ref={emailRef} required />
              </Form.Group>
              <Form.Group id="password">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" ref={passwordRef} required />
              </Form.Group>
              
              <Button className="w-100 mt-4" type="submit">
                Sign In
              </Button>
            </Form>
          </Card.Body>
        </Card>
      </div>
      <div className="w-100 text-center mt-2">
        Have no account? <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Sign up</a>
      </div>
    </>
  );
}

export default SignIn;
