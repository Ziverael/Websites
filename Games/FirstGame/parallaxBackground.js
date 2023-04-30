const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");
const CANVAS_HEIGHT = canvas.height = 700;
const CANVAS_WIDTH = canvas.width = 800;

let gameSpeed = 5;
// let gameFrame = 0; //This is an alternative way

const bgLayer1 = new Image();
bgLayer1.src = 'Images/layer1.png';
const bgLayer2 = new Image();
bgLayer2.src = 'Images/layer2.png';
const bgLayer3 = new Image();
bgLayer3.src = 'Images/layer3.png';
const bgLayer4 = new Image();
bgLayer4.src = 'Images/layer4.png';
const bgLayer5 = new Image();
bgLayer5.src = 'Images/layer5.png';

window.addEventListener("load", function(){
    const gameSpeedChanger = document.querySelector("input");
    const gameSpeedDisplay = document.querySelector("span");

    gameSpeedChanger.value = gameSpeed;
    gameSpeedDisplay.innerText = gameSpeed;

    gameSpeedChanger.addEventListener("change", (e) => {
        gameSpeed = e.target.value;
        gameSpeedDisplay.innerText = gameSpeed;
    })


    class Layer{
        constructor(image_, speed_){
            this.x = 0;
            this.y = 0;
            this.width = image_.width;
            this.height = image_.height;
            this.image = image_;
            this.speedMod = speed_;
            this.speed = gameSpeed * this.speedMod;
        }
        update(){
            this.speed = gameSpeed * this.speedMod;
            if(this.x <= -this.width) this.x = 0;
            this.x = Math.floor(this.x - this.speed);
            // this.x = gameFrame * this.speed % this.width; //This is an alternative way
        }
        draw(){
            ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
            ctx.drawImage(this.image, this.x + this.width, this.y, this.width, this.height);
        }
    }

    const bgArr = [
        new Layer(bgLayer1, 1),
        new Layer(bgLayer2, .5),
        new Layer(bgLayer3, 2),
        new Layer(bgLayer4, .7),
        new Layer(bgLayer5, 1.2)
    ];

    function animate(){
        ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        bgArr.forEach(layer => {
            layer.update();
            layer.draw();
        });
        // gameFrame--; //This is an alternative way
        requestAnimationFrame(animate);
    }
    animate();
})
