import React, { useState } from 'react';
import { Button, Modal } from 'react-bootstrap';

const WarningModal = () => {
    const [show, setShow] = useState(true);

    const handleClose = () => {
        setShow(false);
        window.location.href = '/';
    }
    const handleShow = () => setShow(true);

    return (
        <div>
            {/*<Button variant="primary" onClick={handleShow}>*/}
            {/*    Открыть модальное окно*/}
            {/*</Button>*/}

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Error</Modal.Title>
                </Modal.Header>
                <Modal.Body><b>You are not authorized</b></Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default WarningModal;
