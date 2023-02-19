const sect1 = document.querySelector("section");

//Effect 1 TO DO//
const bl = document.querySelector(".block");
window.addEventListener('keydown', moveBlock);

function moveBlock(e){
    switch(e.code){
        case 'ArrowUp':
            var pos = bl.style.top;

            console.log("UP")
            
        break;
    
    }
}

//Effect 2//
const sect2 = document.querySelector("section:nth-of-type(2)")
const light = {
    "light" : document.getElementById("light"),
    "container" : document.getElementById("lightContainer")
}

sect2.addEventListener('mouseover', (e) => {
    // moveElement(light.container)}) TODO
console.log(el.offsetX)
el.style.left = `${el.clientX}px`
sect2.addEventListener('mouseenter', (e) => {showElement(light.container)})
sect2.addEventListener('mouseleave', (e) => {hideElement(light.container)})

function showElement(el){
    el.style.opacity = "1";
}
function hideElement(el){
    el.style.opacity = "0";
}

function moveElement(e){
}