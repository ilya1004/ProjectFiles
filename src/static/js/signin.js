function checkString(str) {
    let isValid = true;
    var regex = /^[a-zA-Z0-9_.!?<>-]+$/;   // Допустимые символы для строки
    if (str.length > 50 || !regex.test(str)) {
        isValid = false;
    }
    return isValid;
}

function checkEnterForm(el) {
    var login = el.login.value;
    var password = el.password.value;

    var isValid = true;

    if (!checkString(login) || !checkString(password)) {
        isValid = false;
    }

    console.log(login + '\n' + password);

    return isValid;
}
