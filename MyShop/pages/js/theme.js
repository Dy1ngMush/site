document.querySelector('.theme').addEventListener('input', darkmode)
document.addEventListener('DOMContentLoaded', onload)

function darkmode() {
    const main = document.querySelector("main")
    const a = document.querySelectorAll("main a")
    const goods = document.querySelectorAll("main .good")
    const wasDarkMode = localStorage.getItem('darkmode') === 'true'

    localStorage.setItem('darkmode', !wasDarkMode)
    main.classList.toggle('dark-mode', !wasDarkMode)

    a.forEach(function(elem){
        elem.classList.toggle('dark-mode', !wasDarkMode)
    })
    goods.forEach(function(elem){
        elem.classList.toggle('dark-mode', !wasDarkMode)
    })
 }


 function onload() {
    if (sessionStorage.get != null){

    }
    if (localStorage.getItem('darkmode') === 'true'){document.getElementById('theme').checked = true}
    document.querySelector("main").classList.toggle('dark-mode', localStorage.getItem('darkmode') === 'true')
    document.querySelectorAll("main .good").forEach(function(elem){elem.classList.toggle('dark-mode', localStorage.getItem('darkmode') === 'true')})
    document.querySelectorAll("main a").forEach(function(elem){elem.classList.toggle('dark-mode', localStorage.getItem('darkmode') === 'true')})
 }

if (document.getElementById('open_pop_up_signup') != null){
    const openPopUpSignUp = document.getElementById('open_pop_up_signup');
    const popUpSignUp = document.getElementById('pop_up_signup');
    const closePopUpSignUp = document.getElementById('pop_up_close_signup');

    const su_login = document.getElementById('su_login');
    const su_email = document.getElementById('su_email');
    const su_pass = document.getElementById('su_password');
    const su_pass2 = document.getElementById('su_password2');

    openPopUpSignUp.addEventListener('click', function(e){
        e.preventDefault();
        popUpSignUp.classList.add('active');
    })

    closePopUpSignUp.addEventListener('click', () => {
       popUpSignUp.classList.remove('active');
       su_login.value='';su_email.value='';su_pass.value='';su_pass2.value='';
    })


    const openPopUpSignIn = document.getElementById('open_pop_up_signin');
    const popUpSignIn = document.getElementById('pop_up_signin');
    const closePopUpSignIn = document.getElementById('pop_up_close_signin');

    const email = document.getElementById('email')
    const password = document.getElementById('password')


    openPopUpSignIn.addEventListener('click', function(e){
        e.preventDefault();
        popUpSignIn.classList.add('active');
    })

    closePopUpSignIn.addEventListener('click', () => {
       popUpSignIn.classList.remove('active');
       email.value='';password.value='';
    })
}
