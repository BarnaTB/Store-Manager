document.getElementById('signup-form').addEventListener('submit', registerUser)

const url = 'https://store-manag.herokuapp.com/api/v1/signup'

function registerUser(event) {
    event.preventDefault()
    let username = document.getElementById('username')
    let email = document.getElementById('email')
    let password = document.getElementById('password')

    let token = localStorage.getItem('token')
    let invalid = document.getElementById('invalid')

    fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token},
        body: JSON.stringify({username: username.value, email: email.value, password: password.value})
    })
    .then((response) => response.json())
        .then((data) => {
            if (data.status == "OK"){
                invalid.textContent = '' + data.message
                window.location.replace('./home.html')
            }else{
                invalid.textContent = '' + data.message
            }
            console.log(data)
        })
        .catch((err) => console.log(err), invalid.textContent = "It's not you. It's us! Something went terribly wrong!")
}