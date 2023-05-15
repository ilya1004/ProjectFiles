import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { AuthProvider } from "react-auth-kit";
import { BrowserRouter } from "react-router-dom";
import { Router } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css"

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <AuthProvider
    authType="cookie"
    authName="_auth"
    cookieDomain="window.location.hostname"
    cookieSecure={true}
  >
    <App />
  </AuthProvider>
);
