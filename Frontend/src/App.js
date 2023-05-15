import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";

import ProfilePage from "./pages/ProfilePage";
import SignUp from "./components/SignUp";
import { Container } from "react-bootstrap";
import PlayPage from "./pages/PlayPage";
import { Button } from "react-bootstrap";
import RulesPage from "./pages/Rules";

function App() {
  return (
    <Router>
      <div>
        <div className="page-header">
          <div className="logo ">logo</div>
          
          <ul id="navigation-bar " className="nav-bar">
            <li>
              <Link className="Link" to="/">Home</Link>
            </li>
            <li>
              <Link className="Link" to="myprofile">Profile</Link>
            </li>
            <li>
              <Link className="Link" to="game">Play</Link>
            </li>
            <li>
              <Link className="Link" to="rules">Rules</Link>
            </li>
          </ul>
          
          <div class="header-right"><Button className="btn btn-primary outline-0">Sign up</Button></div>
        </div>

        <Routes>
          <Route
            path="/"
            element={
              <Container style={{ minHeight: "100vh", display: "block", alignItems: "center", justifyContent: "center" }}>
                <SignUp />
              </Container>
            }
          />

          <Route path="myprofile" element={<ProfilePage />} />
          <Route path="rules" element={<RulesPage />} />
          <Route path="game" element={<PlayPage/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
