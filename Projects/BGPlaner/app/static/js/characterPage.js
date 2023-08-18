particlesJS.load('particles-js', '../static/json/particles.json', function() {
    console.log('callback - particles.js config loaded');
});

const bg_effect =  document.querySelector(".bg.effect");

function blur_update(){
    let t = 1e6;
    let angle = 2 * Math.PI / t * (new Date() % t);
    bg_effect.style.filter = `blur(${ 1.5 * (Math.sin(angle) + 1)}em)`;
    requestAnimationFrame(blur_update);
    // console.log(angle)
    // console.log(bg_effect.style.filter)
}
blur_update();