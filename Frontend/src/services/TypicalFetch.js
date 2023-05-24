/*
  @param adress - just a string of certain endpoint adress
*/

import { useState, useEffect } from "react";

function TypicalFetch(adress) {

    const [result, setResult] = useState(0);

    useEffect(() => fetchAdress(), []);

    const fetchAdress = async () => {
        const response = await fetch("https://blablabla"+adress);
        const data = await response.json();
        setResult(data);
    }
    return result? result: 0;
}

function typicalPost (adress, data) {
    const postOnAdress = async () => {
        const response = await fetch("https://blablabla"+adress, {
            method: "POST",
            headers: {
                "Content-Type" : "application/json"
            },
            body: JSON.stringify(data)
        });
    }
}

export default TypicalFetch;