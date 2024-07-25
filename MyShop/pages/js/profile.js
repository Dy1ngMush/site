const formcreateprofile = document.getElementById('create_profile_form');
formcreateprofile.addEventListener('submit', create_profile);

async function create_profile(event){
    event.preventDefault();
    const myFormData = new FormData(formcreateprofile);
    myFormData.append('user_id', getCookie('user_id'))
    var object = {};
    myFormData.forEach(function(value, key){
        object[key] = value;
    });
    var json = JSON.stringify(object)
    await fetch('http://localhost:8000/api/v1/profiles', {
        credentials: "same-origin",
        method: 'POST',
        headers: { "Content-Type": "application/json", "Authrorization": getCookie('access_token')},
        body: json
    })
    window.location = `http://localhost:8000/`
}
