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
const sect2_coords = sect2.getBoundingClientRect()

sect2.addEventListener('mousemove', (e) => {
    var coords = {
        'x' : e.clientX - sect2_coords.left - 10,
        'y' : e.clientY - sect2_coords.top - 10
    }
    
    moveElement(light.container, coords)
})
sect2.addEventListener('mouseenter', (e) => {
    showElement(light.container)
})
sect2.addEventListener('mouseleave', (e) => {hideElement(light.container)})

function showElement(el){
    el.style.opacity = "1";
}
function hideElement(el){
    el.style.opacity = "0";
}

    
function moveElement(el, coords){
    el.style.top = `${coords.y}px`
    el.style.left = `${coords.x}px`
}
