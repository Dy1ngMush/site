const addtocart = document.getElementById('form');
addtocart.addEventListener('submit', addproduct);

async function addproduct(event) {
    event.preventDefault();
    const error = document.getElementById('error-product')
    const product_id = document.getElementById('product-id')
    error.classList.add('hide')
    const add_error = document.getElementById('add-error')
    const add_success = document.getElementById('add-success')
    add_success.classList.add('hide')
    add_error.classList.add('hide')
    const quantity = document.getElementById('quantity')
    data = new URLSearchParams()
    data.append('product_id', product_id.innerHTML);
    data.append('quantity', quantity.value)
    if (getCookie('access_token')){
        await fetch(`http://localhost:8000/api/v1/carts/add_product?product_id=${product_id.innerHTML}&quantity=${quantity.value}`, {
            credentials: "same-origin",
            method: 'POST',
            headers: { "Content-Type": "application/json", "Authrorization": getCookie('access_token')},
        }).then(function(response){
        if (response.status == 200){
            add_success.classList.remove('hide')
        }
        else {
            add_error.classList.remove('hide')}
        })
    }
    else {
        error.classList.remove('hide')
    }
}