document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#auth-form div a').addEventListener('click', swapButton);
    document.querySelector('#auth-form button').addEventListener('click', login);
});

function swapButton(e) {
    const button = document.querySelector('#auth-form button');
    const swapText = document.querySelector('#auth-form div p');
    const swapLink = document.querySelector('#auth-form div a');

    if (button.textContent === 'Войти') {
        button.textContent = 'Зарегистрироваться';
        swapText.textContent = 'Уже есть аккаунт?';
        swapLink.textContent = 'Войти';
        button.removeEventListener('click', login);
        button.addEventListener('click', register);
    } else {
        button.textContent = 'Войти';
        swapText.textContent = 'Нет аккаунта?';
        swapLink.textContent = 'Регистрация';
        button.removeEventListener('click', register);
        button.addEventListener('click', login);
    }
}

function login(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const jsonData = JSON.stringify({'email': email, 'password': password});

    fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonData,
        credentials: 'include'
    })
        .then (response => response.json())
        .then (data => {
            if (data['error']) {
                console.log(data['error']);
                alert('Ошибка входа');
            } else {
                document.cookie = `access_token=${data['access_token']}`
                document.cookie = `refresh_token=${data['refresh_token']}`
                location.replace('index.html');
            }
        })
        .catch ((error) => {
            console.log(error);
            alert('Ошибка браузера');
        })
}

function register(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const jsonData = JSON.stringify({'email': email, 'password': password});

    fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonData,
        credentials: 'include'
    })
        .then (response => response.json())
        .then (data => {
            if (data['error']) {
                console.log(data['error']);
                alert('Ошибка регистрации');
            } else {
                location.replace('index.html');
            }
        })
        .catch ((error) => {
            console.log(error);
            alert('Ошибка браузера');
        })
}
