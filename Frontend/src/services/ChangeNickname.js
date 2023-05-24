import React, { useState } from 'react';
import { Button} from "react-bootstrap";
import "../css/Profile.css"

const BASE_URL = `http://localhost:8000`
const url_change_nickname = BASE_URL + `/user/change_curr_user_nickname`;

const ChangeNickname = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const [isButtonHidden, setIsButtonHidden] = useState(false);

    const openPopup = () => {
        setIsOpen(true);
        setIsButtonHidden(true);
    };

    const closePopup = () => {
        setIsOpen(false);
        setIsButtonHidden(false);
    };

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = () => {
        console.log(inputValue);
        console.log(typeof inputValue)

        fetch(url_change_nickname + `?new_nickname=${inputValue}`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                console.log(data);
            });
        closePopup();
    };

    return (
        <div className="settings-buttons">
            {!isButtonHidden && (
                <Button className="setting-button" onClick={openPopup}>Change Nickname</Button>
            )}
            {isOpen && (
                <div>
                    <div>Enter the nickname:</div>
                    <input type="text" className="input-group-text" value={inputValue} onChange={handleInputChange} />
                    <div className="change-nickname-buttons">
                        <Button className="input-buttons" onClick={handleSubmit}>Submit</Button>
                        <Button className="input-buttons" onClick={closePopup}>Cancel</Button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChangeNickname;
