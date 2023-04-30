const canvas = document.getElementById("Canv");
const ctx = canvas.getContext("2d");

const CANVAS_WIDTH = canvas.width = 600;
const CANVAS_HEIGTH = canvas.height = 600;
const SPRITE_SHEET_WIDTH = 6900;
const SPRITE_SHEET_HEIGTH = 5230;
const SPRITE_WIDTH = SPRITE_SHEET_WIDTH / 12;
const SPRITE_HEIGTH = SPRITE_SHEET_HEIGTH / 10;

let playerState = 'run';
let select = document.querySelector("select");
select.addEventListener('change', (e) => {playerState = e.target.value});

let gameFrame = 0;
const staggerFrames = 5;
const spriteAnimations = [];
const animationStates = [
    {
        name : 'idle',
        frames: 7,
    },
    {
        name : 'jump',
        frames : 7
    },
    {
        name : 'fall',
        frames: 7,
    },
    {
        name : 'run',
        frames: 9,
    },
    {
        name : 'dizzy',
        frames: 11,
    },
    {
        name : 'sit',
        frames: 5,
    },
    {
        name : 'roll',
        frames: 7,
    },
    {
        name : 'bite',
        frames: 7,
    },
    {
        name : 'ko',
        frames: 12,
    },
    {
        name : 'getHit',
        frames: 4,
    }
];
animationStates.forEach(
    (state, index) => {
        let frames = {
            loc: []
        }
        for(let j = 0; j < state.frames; j++){
            let posX = j * SPRITE_WIDTH;
            let posY = index * SPRITE_HEIGTH;
            frames.loc.push({x : posX, y : posY});
        }
        spriteAnimations[state.name] = frames;
    }
)

const playerImage = new Image(); /*The same as image tag*/
playerImage.src = 'Images/shadow_dog.png';

function animate(){
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGTH);
    // ctx.fillRect(0, 0, CANVAS_WIDTH / 2, CANVAS_HEIGTH / 2);
    let position = Math.floor(gameFrame / staggerFrames) % spriteAnimations[playerState].loc.length;
    let frameX = SPRITE_WIDTH * position;
    let frameY = spriteAnimations[playerState].loc[position].y;
    ctx.drawImage(
        playerImage,                                        /*Image object*/
        frameX, frameY,                                       /*Position of the image slice*/
        SPRITE_WIDTH, SPRITE_HEIGTH,                        /*size of the image slice*/
        0, 0,                                               /*Coordinates in canvas */
        CANVAS_WIDTH, CANVAS_HEIGTH                         /*size in canvas*/
        )
    gameFrame++;
    requestAnimationFrame(animate);
}
animate();
