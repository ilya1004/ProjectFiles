import React, { useState } from 'react';
import { Button, Modal } from 'react-bootstrap';

const GameEndModal = (props) => {
    const [show, setShow] = useState(true);

    const handleClose = () => {setShow(false); window.location.href = "/selectmode"};
    const handleShow = () => setShow(true);

    return (
        <div>
            {/*<Button variant="primary" onClick={handleShow}>*/}
            {/*    Открыть модальное окно*/}
            {/*</Button>*/}

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>{props.isWin? "You've won" : "You've lost"}</Modal.Title>
                </Modal.Header>
                <Modal.Body><b></b></Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        To Game page
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default GameEndModal;
