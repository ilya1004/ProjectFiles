import axios from "axios";
import React from "react";


function checkString(str) {
    let isValid = true;
    let regex = /^[a-zA-Z0-9_.!?<>-]+$/;   // Допустимые символы для строки
    if (str.length > 50 || !regex.test(str)) {
        isValid = false;
    }
    return isValid;
}

function checkRegForm(el) {
    var nickname = el.nickname.value;
    var login = el.login.value;
    var password = el.password.value;
    var repass = el.repass.value;

    var isValid = true;

    if (!checkString(nickname) || !checkString(login) || !checkString(password) || !checkString(repass)) {
        isValid = false;
    }
    if (password !== repass) {
        isValid = false;
    }

    console.log(nickname + '\n' + login + '\n' + password + '\n' + repass);

    return isValid;
}

