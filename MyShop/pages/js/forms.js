const form = document.getElementById('signup-form');

form.addEventListener('submit', saveuser);

async function saveuser(event) {
    event.preventDefault();
    const myFormData = new FormData(form);
    const password = myFormData.get('password')
    const password2 = myFormData.get('password2')
    const error = document.querySelector('.error.signup')
    for(let data of myFormData){
        console.log(data)
    }
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
        console.log(object)
        var json = JSON.stringify(object)
        await fetch('http://localhost:8000/api/v1/users', {
            credentials: "same-origin",
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: json,
            
            
        })
        
        await fetch('http://localhost:8000/api/v1/tokens', {
            credentials: "same-origin",
            method: 'POST',
            headers: { "Content-Type": 'application/json'},
            body: json,
        }).then(function(response) {
            if (!response.ok){
                console.log('ааа')
            }
            return response.json();
        }).then(function(data){
            sessionStorage.setItem('access_token', data.access_token)
            console.log(sessionStorage.getItem('access_token'))
        })

    }
}