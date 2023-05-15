import React, { Fragment, useRef } from "react";
import { Form, Button, Card } from "react-bootstrap";

function SignUp() {
  const nickRef = useRef();
  const emailRef = useRef();
  const passwordRef = useRef();
  const passwordConfirmRef = useRef();

  function handleSubmit(e) {
    e.preventDefault();
    console.log("Sign up handler called");
  }
  return (
    <>
      <div className="justify-content-center d-flex mt-5">
        <Card>
          <Card.Body>
            <h2 className="text-center mb-4">Sign Up</h2>
            <Form onSubmit={handleSubmit}>
              <Form.Group id="nick">
                <Form.Label>Nickname</Form.Label>
                <Form.Control type="nick" ref={nickRef} required />
              </Form.Group>
              <Form.Group id="email">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" ref={emailRef} required />
              </Form.Group>
              <Form.Group id="password">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" ref={passwordRef} required />
              </Form.Group>
              <Form.Group id="password-confirm">
                <Form.Label>Password Confirmation</Form.Label>
                <Form.Control
                  type="password-confirm"
                  ref={passwordConfirmRef}
                  required
                />
              </Form.Group>
              <Button className="w-100 mt-4" type="submit">
                Sign Up
              </Button>
            </Form>
          </Card.Body>
        </Card>
      </div>
      <div className="w-100 text-center mt-2">
        Already have an account? Log In
      </div>
    </>
  );
}

export default SignUp;
