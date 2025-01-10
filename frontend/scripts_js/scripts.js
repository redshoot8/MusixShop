document.addEventListener('DOMContentLoaded', async () => {
    window.localStorage.removeItem('user-email');
    const email = await getUserEmail();
    if (email) {
        const authLink = document.getElementById('auth-link');
        authLink.style.display = 'none';

        const authorizedUser = document.getElementById('authorized-user');
        authorizedUser.style.display = 'flex';

        const emailElement = authorizedUser.querySelector('p');
        emailElement.textContent = email;
        window.localStorage.setItem('user-email', email);
    }
});

async function getUserEmail() {
    try {
        const response = await xmlHttpWithAuth('GET', 'http://localhost:8000/api/auth/email', {
            ContentType: 'application/json'
        });
    
        if (response === null) {
            throw new Error('Failed to fetch email');
        }
        
        return response.email;
    } catch (error) {
        console.error(error);
        return null;
    }
}

async function xmlHttpWithAuth(method, url, options = {}) {
    let cookie = getCookie();
    let xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', options.ContentType);
    xhr.setRequestHeader('credentials', 'include');
    xhr.setRequestHeader('access-token', cookie['access_token']);

    return new Promise((resolve, reject) => {
        xhr.onload = function () {
            if (xhr.status === 200) {
                console.log(xhr.responseText);
                const response = JSON.parse(xhr.responseText);
                resolve(response);
            } else if (xhr.status === 401) {
                cookie = getCookie();
                let RefreshXhr = new XMLHttpRequest();
                RefreshXhr.open('POST', 'http://localhost:8000/api/auth/refresh', true);
                RefreshXhr.setRequestHeader('Content-Type', 'application/json');
                RefreshXhr.setRequestHeader('credentials', 'include');
                RefreshXhr.setRequestHeader('refresh-token', cookie['refresh_token']);
                
                RefreshXhr.onload = function () {
                    if (RefreshXhr.status === 200) {
                        const response = JSON.parse(RefreshXhr.responseText);
                        if (response['access_token']) {
                            document.cookie = `access_token=${response['access_token']}`;
                        }
                    } else {
                        throw new Error('Failed to refresh tokens');
                    }
                }

                RefreshXhr.onerror = function () {
                    console.log('Ошибка запроса на обновление токена');
                    return null;
                }
                
                RefreshXhr.send();

                cookie = getCookie();
                let secondXhr = new XMLHttpRequest();
                secondXhr.open(method, url, true);
                secondXhr.setRequestHeader('Content-Type', options.ContentType);
                secondXhr.setRequestHeader('credentials', 'include');
                secondXhr.setRequestHeader('access-token', cookie['access_token']);
                secondXhr.setRequestHeader('access-token', cookie['access_token']);

                secondXhr.onload = function () {
                    if (secondXhr.status === 200) {
                        console.log(secondXhr.responseText);
                        const response = JSON.parse(secondXhr.responseText);
                        resolve(response);
                    }
                }

                secondXhr.send();
            } else {
                reject(new Error(`HTTP error! status: ${xhr.status}`));
            }
        }

        xhr.onerror = function () {
            console.log('Ошибка запроса на получение email');
        }

        xhr.send();
    });
}


function getCookie() {
    return document.cookie.split('; ').reduce((acc, item) => {
        const [name, value] = item.split('=')
        acc[name] = value
        return acc
    }, {})
}
