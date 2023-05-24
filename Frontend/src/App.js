import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import Profile from "./pages/ProfilePage";
import PlayPage from "./pages/PlayPage";
import RulesPage from "./pages/RulesPage";
import SignUp from "./pages/SignUpPage";
import HomePage from "./pages/HomePage";
import LogoImage from "./img/logo.jpg"
import Login from "./pages/LoginPage";
import SelectModePage from "./pages/SelectModePage";
import GamePage from "./pages/GamePage (old)";
import ListsInfo from "./pages/ListsInfoPage";
// import ChooseModePage from "./pages/ChooseModePage";

function App() {
    return (
        <Router>
        <div>
            <div className="page-header">
                <div className="logo">
                    <img className="logo-img" src={LogoImage} alt="Error"/>
                </div>
            <ul id="navigation-bar " className="nav-bar">
                <li>
                    <Link className="Link" to="home">Home</Link>
                </li>
                <li>
                    <Link className="Link" to="board">Board</Link>
                </li>
                {/*<li>*/}
                {/*    <Link className="Link" to="selectmode">Play</Link>*/}

                    {/*<Link className="Link" to="choosemode">Play</Link>*/}
                {/*</li>*/}
                <li>
                    <Link className="Link" to="rules">Rules</Link>
                </li>
                <li>
                    <Link className="Link" to="listsinfo">Information</Link>
                </li>
                <li>
                    <Link className="Link" to="myprofile">Profile</Link>
                </li>
                <li>
                    <Link className="Link" to="/">Log In</Link>
                </li>
          </ul>
        </div>

        <Routes>
            <Route path="home" element={<HomePage/>} />
            <Route path="board" element={<PlayPage/>} />
            <Route path="rules" element={<RulesPage  />} />
            <Route path="listsinfo" element={<ListsInfo />} />
            <Route path="myprofile" element={<Profile />} />
            <Route path="/" element={<Login/>} />
            {/*<Route path="selectmode" element={<SelectModePage/>} />*/}
            <Route path="game" element={<GamePage/>} />
            <Route path="reg" element ={<SignUp/>} />

            {/*<Route path="/reg" element ={<SignUp/>} />*/}
            {/*<Route path="/choosemode" element = {<ChooseModePage/>}/>*/}
          {/*<Route path="rules" element = {<SignUpPage/>} />*/}


        </Routes>
        </div>
    </Router>
  );
}

export default App;
