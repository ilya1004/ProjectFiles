import axios from "axios";

function RulesPage() {
    return (
        <div className="qwe">
            <h1>МАКСИМ ИДИ РАБОТАЙ</h1>
            <button onClick={handleClick}>Click me</button>
        </div>
    );
}


function handleClick() {
    console.log("request")

    const user_id = 4;
    let url1 = 'http://localhost:8000/user/get_info_by_user_id?user_id=${user_id}';
    let url2 = "http://localhost:8000/user/get_info_of_all_users";

    let qwe;
    let responce = axios.get(`http://localhost:8000/user/get_info_by_user_id?user_id=${user_id}`)
        .then(response => {
            console.log(response.data);
            if (response.data) {
                qwe = response.data;
                console.log(qwe)
            }
            // qwe = response.data;
        })

}


export default RulesPage;
