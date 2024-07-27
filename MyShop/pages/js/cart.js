const addtoorder = document.getElementById('create-order');
addtoorder.addEventListener('submit', addorder);

const cross = document.querySelectorAll('.cross');
cross.forEach(function(elem){
    elem.addEventListener('click', deleteproduct);
})

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

async function deleteproduct(event){
    event.preventDefault();
    product_id = event.target.parentElement.querySelector('.hide').innerText
    await fetch(`http://localhost:8000/api/v1/carts/delete_one_product/${product_id}`,
    {
        credentials: "same-origin",
        method: 'DELETE',
        headers: { "Content-Type": "application/json", "Authrorization": getCookie('access_token')},
    })
    location.reload()
}