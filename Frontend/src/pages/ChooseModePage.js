import { Button } from "react-bootstrap";
import { Card } from "react-bootstrap";
import classes from "./ChooseModePage.module.css";
import { useState } from "react";

function ChooseModePage() {
  const [isRate, setRate] = useState(false);

  const changeRate = (e, val) => {
    e.preventDefault();
    setRate(val);
    console.log(isRate);
  };

  const handleClick = (e, id) => {
    e.preventDefault();
    console.log(e);
    console.log(id);
    window.location.href = "/game";
  };

  return (
    <div className={classes.page}>
      <h2 className={classes.head}>Belarusian Chess</h2>
      <div className= {classes.cont}>
        <div className={classes.row}>
          <Button style={!isRate? {backgroundColor: "darkblue"} : {backgroundColor: "lightgray"}} type="button" onClick={(e) => changeRate(e, false)}>
            Unrated
          </Button>
          <Button style={!isRate? {backgroundColor: "lightgray"} : {backgroundColor: "darkblue"}} type="button" onClick={(e) => changeRate(e, true)}>
            Rated
          </Button>
        </div>
        <div className={classes.row}>
          <Button type="button" onClick={(e) => handleClick(e, "Blitz1")}>
            Blitz
          </Button>{" "}
          <Button type="button" onClick={(e) => handleClick(e, "Blitz2")}>
            Blitz
          </Button>
          <Button type="button" onClick={(e) => handleClick(e, "Blitz3")}>
            Blitz
          </Button>
        </div>
        <div className={classes.row}>
          <Button type="button" onClick={(e) => handleClick(e, "Rapid1")}>
            Rapid
          </Button>
          <Button type="button" onClick={(e) => handleClick(e, "Rapid2")}>
            Rapid
          </Button>
          <Button type="button" onClick={(e) => handleClick(e, "Rapid3")}>
            Rapid
          </Button>
        </div>
        <div className={classes.row}>
          <Button type="button" onClick={(e) => handleClick(e, "Classical1")}>
            Classical
          </Button>
          <Button type="button" onClick={(e) => handleClick(e, "Classical2")}>
            Classical
          </Button>
          <Button type="button" onClick={(e) => handleClick(e, "Classical3")}>
            Classical
          </Button>
        </div>
      </div>
    </div>
  );
}

export default ChooseModePage;
