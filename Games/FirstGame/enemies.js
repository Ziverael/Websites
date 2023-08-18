/** @type {HTMLCanvasElement} */
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext('2d');

const CANVAS_WIDTH = canvas.width = 800;
const CANVAS_HEIGHT = canvas.height = 700;
const numberOfEnemies = 100;
const enemiesArray = [];
let gameFrame = 0;

const enemyImage1 = new Image();
enemyImage1.src = "/Images/enemy1.png";


const enemyType = {
    "Type1" : {
        width : 100,
        height : 100,
        speed : () =>{return [Math.random() * 4 - 2, Math.random() * 4 - 2]},
        img : enemyImage1,
        sheetWidth : 1758,
        sheetHeight : 155,
        frames : 6
    }
}

class Enemy{
    constructor(x_, y_, type_){
        this.x = x_;
        this.y = y_;
        [this.speedX, this.speedY] = enemyType[type_].speed();
        this.image = enemyType[type_].img;
        this.spriteWidth = enemyType[type_].sheetWidth / enemyType[type_].frames;
        this.spriteHeight = enemyType[type_].sheetHeight,
        this.width = this.spriteWidth / 2.5;
        this.height = this.spriteHeight / 2.5;
        this.framesTotal = enemyType[type_].frames - 1;
        this.frame = 0;
        this.flapSpeed = Math.floor(Math.random() * 3 + 1);
    }

    update(){
        this.x += this.speedX;
        this.y += this.speedY;
        /*Wiggling*/
        this.x += Math.random() * 2 - 1;
        this.y += Math.random() * 2 - 1;
        if(gameFrame % 2 === 0) this.frame >= this.framesTotal ? this.frame = 0 : this.frame++;
    }

    draw(){
        ctx.drawImage(
            this.image,
            this.frame * this.spriteWidth, 0,
            this.spriteWidth, this.spriteHeight,
            this.x, this.y,
            this.width, this.height);
    }
}


for(let i = 0; i < numberOfEnemies; i++){
    enemiesArray.push(new Enemy(Math.random() * (CANVAS_WIDTH - 200), Math.random() * (CANVAS_HEIGHT - 200), "Type1"));
}


function animate(){
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    enemiesArray.forEach(enemy => {
        enemy.update();
        enemy.draw();
    })
    gameFrame++;
    requestAnimationFrame(animate);
}
animate();