// ---------------------------
// ---------------------------
// ---------------------------
// -----------BUTTONS---------
// ---------------------------
// ---------------------------

function wave(e){
    let spot = document.createElement("div")
    spot.classList.toggle("button-blob");
    spot.style.top = `${e.layerY}px`;
    spot.style.left = `${e.layerX}px`;
    // spot.style.clipPath = `circle(0 at ${e.layerX}px ${e.layerY}px)`
    // console.log(spot.style.clipPath);
    //e.currentTarget == this in this problem 
    e.currentTarget.appendChild(spot);

    
    // Remove ripples
    setTimeout(() => {spot.remove()}, 400)
}

let buttons = document.querySelectorAll(".button");
for(button of buttons){
    console.log(button)
    button.addEventListener("click", wave, button);
}