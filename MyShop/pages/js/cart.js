const addtoorder = document.getElementById('create-order');
addtoorder.addEventListener('submit', addorder);

async function addorder(event) {
    event.preventDefault();
    const add_error = document.getElementById('add-error')
    const value = document.getElementById('summ').innerText.slice(0,-2)
    add_error.classList.add('hide')
    if (value != "0"){
    await fetch('http://localhost:8000/api/v1/orders', {
        credentials: "same-origin",
        method: 'POST',
        headers: { "Content-Type": "application/json", "Authrorization": getCookie('access_token')},
        }).then(function(response){
            window.location = `http://localhost:8000/orders/${getCookie('user_id')}`;
       })
    }
    else{
    add_error.classList.remove('hide')
    }
}