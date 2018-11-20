document.getElementById('login-form').addEventListener('submit', loginUser)

const url = 'http://localhost:5000/api/v1/login'

function loginUser(event) {
    event.preventDefault()
    let username = document.getElementById('username')
    let password = document.getElementById('password')
    let invalid = document.getElementById('invalid')

    fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username.value, password: password.value})
    })
    .then((response) => response.json())
        .then((data) => {
            if (data.message == "Logged in!"){
                window.location.replace('../Store-Manager/UI/templates/home.html')
                localStorage.setItem('token', data.token)
            }else{
                invalid.textContent = '' + data.message
            }
            console.log(data)
        })
        .catch((err) => console.log(err), invalid.textContent = '' + data.message)
}