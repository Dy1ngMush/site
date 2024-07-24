const formsignup = document.getElementById('signup-form');
formsignup.addEventListener('submit', saveuser);

const formsignin = document.getElementById('signin-form');
formsignin.addEventListener('submit', checkuser);


async function saveuser(event) {
    event.preventDefault();
    const myFormData = new FormData(formsignup);
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
        formsignup.classList.add('hide')



    }
}

async function checkuser(event){
    event.preventDefault();

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
        sessionStorage.setItem('access_token', data.access_token)
    })

}

