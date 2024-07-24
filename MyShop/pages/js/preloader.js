let p = $('.preloader');
if (localStorage.getItem('darkmode') === 'true'){
    p.css('background-color', '#333333')
}
else {
    p.css('background-color', "#a3a4a8")
}
function preloader() {
    setInterval(() => {
        $(() => {
            p.css('opacity', 0);
            setInterval(
                () => p.remove(),
                200
            );
        });
    }, 200);
}

preloader()