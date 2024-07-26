if (document.querySelector('#signup-form')){
const formsignup = document.getElementById('signup-form');
formsignup.addEventListener('submit', saveuser);
}
if (document.querySelector('#signin-form')){
const formsignin = document.getElementById('signin-form');
formsignin.addEventListener('submit', checkuser);
}
if (document.querySelector('#exit-button')){
const exit = document.getElementById('exit-button');
exit.addEventListener('click', async function(){
    await fetch(`http://localhost:8000/api/v1/tokens/{token}?token_id=${getCookie("access_token_id")}`, {
            method: 'DELETE',
            headers: { "Content-Type": "application/json" },
    })
    deleteCookie("access_token_id");
    deleteCookie('access_token');
    deleteCookie('user_id');
    location.reload()
})
}

async function saveuser(event) {
    const formsignup = document.getElementById('signup-form');
    if (getCookie("access_token")){
        deleteCookie('access_token')
    }
    const myFormData = new FormData(formsignup);
    const popUpSignIn = document.getElementById('pop_up_signin');
    const password = myFormData.get('password')
    const password2 = myFormData.get('password2')
    const error = document.querySelector('.error.signup')
    if (password != password2){
        error.classList.remove('hide')
    }
    else{
        error.classList.add('hide')
        myFormData.append('active', JSON.stringify(true))
        myFormData.append('role', 'regular')
        myFormData.delete('password2')
        var object = {};
        myFormData.forEach(function(value, key){
            object[key] = value;
        });
        var json = JSON.stringify(object)
        await fetch('http://localhost:8000/api/v1/users', {
            credentials: "same-origin",
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: json,
        })
        location.reload()

    }
}

async function checkuser(event){
    event.preventDefault();
    const formsignin = document.getElementById('signin-form');
    if (getCookie("access_token")){
        deleteCookie('access_token')
    }
    const myFormData = new FormData(formsignin);
    const error403 = document.getElementById('403')
    const error404 = document.getElementById('404')
    const error500 = document.getElementById('500')
    error500.classList.add('hide')
    error404.classList.add('hide')
    error403.classList.add('hide')
    myFormData.append('active', JSON.stringify(true))
    myFormData.append('role', 'regular')
    myFormData.append('username', '')
    var object = {};
    myFormData.forEach(function(value, key){
        object[key] = value;
    });
    var json = JSON.stringify(object)
    await fetch('http://localhost:8000/api/v1/tokens', {
        credentials: "same-origin",
        method: 'POST',
        headers: { "Content-Type": 'application/json'},
        body: json,
    }).then(function(response) {
        if (response.status === 404){
            error404.classList.remove('hide')
        }
        else if (response.status === 403){
            error403.classList.remove('hide')
        }
        else if (response.status === 500){
            error500.classList.remove('hide')
        }
        return response.json();
    }).then(function(data){
        setCookie('access_token', data.access_token)
        setCookie('access_token_id', data.id)
    })
    var object = {'access_token': getCookie('access_token')}
    var json = JSON.stringify(object)
    console.log(json)
    await fetch('http://localhost:8000/api/v1/tokens/get_user_id', {
        credentials: "same-origin",
        method: 'POST',
        headers: { "Content-Type": 'application/json'},
        body: json,
        }).then(function(response) {
        return response.json();
        }).then(function(data){
            setCookie('user_id', data)
        })
    user_id = getCookie("user_id")
    await fetch('http://localhost:8000/api/v1/cart', {
        credentials: "same-origin",
        method: "GET",
        headers: { "Content-Type": 'application/json', "Authrorization": getCookie('access_token')}
    }).then(function(response){
        if (response.status != 200){
        fetch('http://localhost:8000/api/v1/carts', {
            credentials: "same-origin",
            method: 'POST',
            headers: { "Content-Type": 'application/json', "Authrorization": getCookie('access_token')},
            body: JSON.stringify({'user_id': user_id})
            })
        }
    })
    await fetch('http://localhost:8000/api/v1/profiles', {
        credentials: "same-origin",
        method: 'GET',
        headers: { "Content-Type": 'application/json', "Authrorization": getCookie('access_token')},
    }).then(function(response){
    if (response.status != 200){
        window.location = `http://localhost:8000/create_profile/${getCookie('user_id')}`;
    }
    else {
        location.reload()
    return response.json();
    }
    })
}