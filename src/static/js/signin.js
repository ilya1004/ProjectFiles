function checkForm(el) {

    var name = el.name.value;
    var password = el.password.value;
    var repass = el.repass.value;
    var state = el.state.value;
    var isdoter = el.isdoter.value;

    console.log(name + '\n' + password + '\n' + repass + '\n' + state + '\n' + isdoter);

    return false;
}
