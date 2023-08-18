////////////VARIABLES////////////
/////CONST////
/////JSON////
let BACKGROUND = {}
fetch("../static/json/backgrounds.json")
    .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        BACKGROUND = data;
  })

let SPECIALIZATION = {}
fetch("../static/json/specializations.json")
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
      SPECIALIZATION = data;
})

let SUBRACES = {}
fetch("../static/json/subraces.json")
    .then(function(resopnse){
        return resopnse.json();
    })
    .then(function(data){
        SUBRACES = data;
    })
/////DOM////
const form = document.querySelector("form");
const buttonSendForm = document.getElementById("CreatePlayer")
const character_ =  document.getElementById("Character")

const variant_ = document.getElementById("variant");

const srFields = document.querySelectorAll("#SubraceInputs .field");

const bgInputs = document.querySelectorAll("#BackgroundInputs input")
const bgFields = document.querySelectorAll("#BackgroundInputs .field");

const specInputs = document.querySelectorAll("#SpecializationInputs input");
const specFields = document.querySelectorAll("#SpecializationInputs .field");
const specFocusSkills = document.querySelector("#SpecializationInputs .field:last-of-type > div")




////////////CLASSES////////////
class Player{
    constructor(name, surename, gender, race, subrace, background, spec, args = "")
    {
        this.abilities = {
            "agility" : 0,
            "fortitude" : 0,
            "instinct" : 0,
            "intelligence" : 0,
            "strength" : 0,
            "willpower" : 0
        }

        this.skills = {
            "acrobatics" : 0,
            "athletics" : 0,
            "computers" : 0,
            "defensive training" : 0,
            "durability" : 0,
            "endurance" : 0,
            "influence" : 0,
            "leadership" : 0,
            "lore" : 0,
            "medicine" : 0,
            "melee" : 0,
            "mental training" : 0,
            "perception" : 0,
            "pilot" : 0,
            "psionic" : 0,
            "ranged" : 0,
            "science" : 0,
            "stealth" : 0,
            "survival" : 0,
            "tactics" : 0,
        }
        
        this.race = race;
        this.name = name;
        this.surename = surename;
        this.gender = gender;

        this.subrace = subrace;
        this.background = background;
        this.spec = spec;
        
        this.traits = [];
        this.min_psi_lvl = 0;
        this.max_psi_lvl = 0;
        
        this.cp =
        25 -                                //Initial value for Heroic Character
        SUBRACES[this.subrace]["CP"] -      //
        BACKGROUND[this.background]["CP"];  //Background cost
        // SPECIALIZATION["CP"];
        console.log([SUBRACES[this.subrace]["CP"], BACKGROUND[this.background]["CP"]])
        if(subrace == "Terran Psionic")
        {
            subrace += args[0];
            this.min_psi_lvl = args[1]["Starting psi level"];
            this.max_psi_lvl = args[1]["Maximum psi level"];
            this.traits.push(args[1]["Available trait"])
            this.cp -= args[1]["CP"];
        }
        
        /*Compute initial abilities*/
        for(const [abil, val] of Object.entries(SUBRACES[this.subrace]["Ability"]))
        {
            this.abilities[abil] += val;
        }
        for(const [abil, val] of Object.entries(BACKGROUND[this.background]["Ability"]))
        {
            this.abilities[abil] += val;
        }
        for(const [abil, val] of Object.entries(SPECIALIZATION[this.spec]["Ability"]))
        {
            this.abilities[abil] += val;
        }
        
        /*Compute initial skills*/
        // for(const [skill, val])
        

        this.hp = 40 + 3 * this.abilities["fortitude"];
        this.healingTreshold = 5 + Math.floor(.5 * this.abilities["fortitude"]);
        // this.damageTreshold = 16 + this.skills["Durability"] + this.abilities["fortitude"];
        
        
        this.moveSpeed = 4 + Math.floor(.5 * this.abilities["agility"]);
        this.shiftSpeed = 1 + Math.floor( .2 * this.abilities["agility"]);
        this.initiative = Math.max(this.abilities["instinct"], this.skills[""])


        
        

        }
        
        // get cp()
        // {
        //     return this.cp;
        // }

        get willpower()
        {
            return this.abilities["willpower"];
        }
        
        get inteligence()
        {
            return this.abilities["intelligence"];
        }

        get agility()
        {
            return this.abilities["agility"];
        }

        get fortitude()
        {
            return this.abilities["fortitude"];
        }
        
        get strength()
        {
            return this.abilities["strength"];
        }

        get instincts()
        {
            return this.abilities["instinct"];
        }

        get ability()
        {
            return this.abilities
        }

        purchaseSkillPoints()
        {
            if(this.cp > 0){
                this.cp--;
                this.sp = this.sp + 2 + Math.floor(0.5 * this.int);
                if(this.race == "Terran"){
                    this.sp++ //Terran bonus
                }
            }
            else{
                console.log("Not enought CP.")
            }
        }

        updatePlayerSheet()
        {
            //For update all fields
        }
}


////////////FUNCTIONS////////////
function new_player(){
    let name_ = prompt("Wprowadź imię bohatera");
    let race_ = prompt("Wprowadź rasę bohatera")
    return pl_ = new Player(name_, race_)
}


function purchaseSkill(skill){
//TO DO
}

function getCP(num){

}

function createPlayer(){
    const data = new FormData(form)
    const args = ""
    if(data.get("variant") == "Terran Psionic")
    {
        const variant_ = data.get("psiVariant")
        args = [variant_, SUBRACES["Terran Psionic"]["Variant"][variant_]];
    }
    
    //Here parse data. If values are valid, then create character
    let player = new Player(
        data.get("name"),
        data.get("surename"),
        data.get("gender"),
        "Terran",           //Actually constant
        data.get("variant"),
        data.get("background"),
        data.get("specialization"),
        args
    )

    console.log(player.cp)
    console.log(player)
    // console.log(player)
    // let character_spec = document.querySelector("#Character ul")

    // const data = {
    //     "name" : document.getElementById("name").value,
    //     "surename" : document.getElementById("surename").value,
    //     "race" : document.getElementById("race").value,
    //     "gender" : document.querySelector("#gender:checked").value,
    //     "background" : document.getElementById("bg").value
    // }

    // character_spec.children[0].children[0].textContent = data["name"];
    // character_spec.children[1].children[0].textContent = data["surename"];
    // character_spec.children[2].children[0].textContent = 5;
    // character_spec.children[3].children[0].textContent = data["race"];
    // character_spec.children[4].children[0].textContent = data["gender"];
    // character_spec.children[6].children[0].textContent = data["background"];

    
}

function switchBackgroundContent(bg_name){
    const select = typeof(bg_name) != "string" ? bg_name.target.value : bg_name;
    const class_ = BACKGROUND[select];
    const cp = class_.CP;
    const ability = class_.Ability;
    const spec = class_.SpecialAbilities;
    const talent = class_["Bonus Talent"];
    const wealth = class_.Wealth;
    const desc = class_.Description;
    // const entries = Object.values(BACKGROUND[bg_name.target.value])

    bgFields[0].childNodes[2].textContent = cp;

    //Set abilities tags
    let i = bgFields[1].childNodes.length - 1;
    while(i > 1){
        bgFields[1].childNodes[i].remove();
        i--;
    }
    // }
    for(abil in ability){
        let header = document.createElement("h4");
        let val = document.createElement("p");
        val.classList.add("value")
        header.innerText = abil;
        val.innerText = ability[abil];
        bgFields[1].append(header);
        bgFields[1].append(val);
    }

    //Set special skills tags
    i = bgFields[2].childNodes.length - 1;
    while(i > 1){
        bgFields[2].childNodes[i].remove();
        i--;
    }
    for(skill in spec){
        let header = document.createElement("h4");
        let desc = document.createElement("p");
        desc.classList.add("desc")
        header.innerText = skill;
        desc.innerText = spec[skill];
        bgFields[2].append(header);
        bgFields[2].append(desc);
    }
    
    bgFields[3].childNodes[2].textContent = talent ? talent : "Brak";
    bgFields[4].childNodes[2].textContent = wealth ? wealth : "Brak";
    bgFields[5].childNodes[2].textContent = desc;



    // for(let i = 0; i < bgFields.length; i++){
    //     bgFields[i].textContent = entries[i];
    // }
}


function switchSpecializationContent(spec_name){
    const select = typeof(spec_name) != "string" ? spec_name.target.value : spec_name;
    const class_ = SPECIALIZATION[select];
    const ability = class_.Ability;
    const spec = class_.SpecialAbilities;
    const talent = class_["Talent"];

    const focus_skill = class_["Focus Skill"].split("|");

    // //Set abilities tags
    let i = specFields[0].childNodes.length - 1;
    while(i > 1){
        specFields[0].childNodes[i].remove();
        i--;
    }
    for(abil in ability){
        let header = document.createElement("h4");
        let val = document.createElement("p");
        val.classList.add("value")
        header.innerText = abil;
        val.innerText = ability[abil];
        specFields[0].append(header);
        specFields[0].append(val);
    }
    specFields[2].childNodes[2].textContent = talent ? talent : "Brak";


    //Set focus skills
    while(specFocusSkills.firstChild){
        specFocusSkills.removeChild(specFocusSkills.firstChild);
    }
    for(let j = 0; j < focus_skill.length; j++){
        // let f_skill = document.createElement("span");//Put here radio button to select

        let f_skill_radio = document.createElement("input");
        let f_skill_label = document.createElement("label");
        f_skill_radio.setAttribute("type", "radio");
        f_skill_radio.setAttribute("id", focus_skill[j]);
        f_skill_radio.setAttribute("name", "focus_skill");
        f_skill_radio.setAttribute("value", focus_skill[j]);

        f_skill_label.setAttribute("for", focus_skill[j]);
        f_skill_label.innerText = focus_skill[j];
        // f_skill.innerText = focus_skill[j];
        // console.log(f_skill)
        specFocusSkills.appendChild(f_skill_radio);
        specFocusSkills.appendChild(f_skill_label);
    }
    // //Set special skills tags
    i = specFields[1].childNodes.length - 1;
    while(i > 1){
        specFields[1].childNodes[i].remove();
        i--;
    }
    for(skill in spec){
        let header = document.createElement("h4");
        let desc = document.createElement("p");
        desc.classList.add("desc")
        header.innerText = skill;
        desc.innerText = spec[skill];
        specFields[1].append(header);
        specFields[1].append(desc);
    }
}

function switchVariantContent(subrace_name){
    const select = typeof(subrace_name) != "string" ? subrace_name.target.value : subrace_name;
    const class_ = SUBRACES[select];
    const cp = class_.CP;
    const ability = class_.Ability;
    const overall_desc = class_["Overall Description"];
    srFields[0].childNodes[2].textContent = cp;
    
    
    //Set abilities tags
    let i = srFields[1].childNodes.length - 1;
    while(i > 1){
        srFields[1].childNodes[i].remove();
        i--;
    }
    for(abil in ability){
        let header = document.createElement("h4");
        let val = document.createElement("p");
        val.classList.add("value")
        header.innerText = abil;
        val.innerText = ability[abil];
        srFields[1].append(header);
        srFields[1].append(val);
    }
    
    i = srFields[2].childNodes.length - 1;
    while(i > 0){
        srFields[2].childNodes[i].remove();
        i--;
    }
    for(const [header_, desc_] of Object.entries(overall_desc))
    {
        let header = document.createElement("h4");
        let desc = document.createElement("p");
        header.append(header_);
        desc.append(desc_);
        srFields[2].append(header);
        srFields[2].append(desc);
    }

    //Destroy psiVar DOM element if exists
    const var_ = document.getElementById("PsiVar");
    if(var_)
        var_.remove();
        
    //For psionic add select field property
    if(class_.hasOwnProperty("Variant"))
    {
        const field = document.createElement("div");
        field.classList.add("field");
        field.setAttribute("id", "PsiVar")
        const header = document.createElement("h4")
        header.innerText = "Poziomy psioniki"
        field.append(header);
        for(const [name_, vals_] of Object.entries(class_["Variant"]))
        {
            const subField = document.createElement("div")
            let spanHead = document.createElement("span")
            let spanDesc = document.createElement("span")
            const innerField = document.createElement("div")
            innerField.classList.toggle("field")
            innerField.append(spanHead)
            innerField.append(spanDesc)
            spanDesc.classList.toggle("value")
            
            // subField.classList.add("field")

            const radioB = document.createElement("input")
            radioB.setAttribute("type", "radio")
            radioB.setAttribute("id", name_)
            radioB.setAttribute("name", "psiVariant")
            radioB.setAttribute("value", name_)
            

            const label_ = document.createElement("label")
            label_.setAttribute("for", name_)
            label_.innerText = name_
            
            subField.append(radioB)
            subField.append(label_)
            for(const [header_, desc_] of Object.entries(vals_))
            {
                spanHead.innerText = header_;
                spanDesc.innerText = desc_;
                subField.appendChild(innerField.cloneNode(true))


            }
            field.append(subField);
        }
        // srFields.appendChild(field);
        document.getElementById("SubraceInputs").append(field);

    }
    
    
}
////////////MAIN////////////
buttonSendForm.addEventListener("click", createPlayer)

for(input_ of bgInputs){
    input_.addEventListener("change", switchBackgroundContent);
}
for(input_ of specInputs){
    input_.addEventListener("change", switchSpecializationContent);
}


buttonSendForm.addEventListener("change", createPlayer)

variant_.addEventListener("change", (variant) => {    
    if(variant.target.value == "TerranPsionic"){
        if(bgInputs[0].hasAttribute("disabled")){
            bgInputs[0].removeAttribute("disabled") ;
        }
    }
    else{
        bgInputs[2].click();
        bgInputs[0].setAttribute("disabled", "");
    }
})
variant_.addEventListener("change", switchVariantContent)


// switchBackgroundContent("CoreCitizen")//Why it doesn;;t work?

// pl1 = new_player()
// const pl1 = new Player("James", "Terran");
 

//Setting values in file
// let abilities = document.getElementById("Ability");
// for(let i = 0; i < abilities.children["length"]; i++){
//     // let abils = pl1.ability;/////////////////////////////////////
//     abilities.children[i].innerText = `${abils[]}`
//     console.log(abilities.children[i].innerText);
// }

