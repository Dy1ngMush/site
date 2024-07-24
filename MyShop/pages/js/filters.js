const filters = document.querySelector('#filters'),
filtersa = document.querySelector('#form'),
allprice = document.querySelectorAll(".price"),
station = document.querySelectorAll("div#station"),
panel = document.querySelectorAll("div#panel");

filters.addEventListener('input', filterGoods);
filtersa.addEventListener('input', filterGoods);

function filterPrice(pricemin, pricemax, elem){
    if (pricemin != "" || pricemax != ""){
        goodprice = elem.children[1].children[2].innerHTML.slice(0, -1)
        if (parseInt(goodprice) < parseInt(pricemin) || parseInt(goodprice) > parseInt(pricemax)){ 
            elem.classList.add('hide')
        }
    }
}

function filterType(type, elem){
    if (type != elem.id && type != "all"){
        elem.classList.add('hide')
    }
}

function filterSearch(){
    let search = document.querySelector(".q1")
    let val = search.value.trim().toLowerCase();
    let elasticItems = document.querySelectorAll('.query div.hidden');
    if (val != '') {
        elasticItems.forEach(function (elem) {
            if (elem.innerText.toLowerCase().search(val) == -1) {
                elem.classList.add('hide');
            }
            else {
                elem.classList.remove('hide');
            }
        });
    }
    else {
        elasticItems.forEach(function (elem){
            elem.classList.remove('hide');
        })
    }
}



function filterGoods() {
    const
    type = filters.querySelector('#type input:checked').value;
    let pricemin = document.querySelector("#price-min").value
    let pricemax = document.querySelector("#price-max").value
    items = document.querySelectorAll(".good")
    items.forEach(function (elem) {
        elem.classList.remove('hide')
    })
    if (type == 'station'){
       document.querySelector('.type-of-battery').classList.remove('hide')
       battery = filters.querySelector('#batter-filter input:checked').value;
    }
    else {
        document.querySelector('.type-of-battery').classList.add('hide')
        document.getElementById('allbattery').checked = true
        document.getElementById('LifeP04').checked = false
        document.getElementById('Lithium-ion').checked = false
    }
    filterSearch()

    items.forEach(function (elem) {
        filterPrice(pricemin, pricemax, elem)
        let hide = Array.from(elem.classList).includes('hide')
        if (hide == true){
            //pass
        }
        else {
            filterType(type, elem)
            if (type == 'station'){
                let elasticItems = document.querySelectorAll('.query div.hidden')
                elasticItems.forEach(function (elem) {
                    if (battery != elem.innerText.slice(-4) && battery != 'allbattery'){
                        console.log(battery, elem.innerText.slice(-4))
                        elem.classList.add('hide')
                    }
                })
            }
        }
    }
)
}