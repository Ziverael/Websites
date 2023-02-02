
//Tags//
let linkBox = document.getElementById('linkBox');
let anchors = document.querySelectorAll("#rank li");

//Here will be elements from database//
let topList = {
    "top1" : {
        "logo" : "Logo",
        "video" : "Video",
        "link" : "link"
    },
    "top2" : {
        "logo" : "Logo",
        "video" : "Video",
        "link" : "link"
    },
    "top3" : {
        "logo" : "Logo",
        "video" : "Video",
        "link" : "link"
    },
    "top4" : {
        "logo" : "Logo",
        "video" : "Video",
        "link" : "link"
    },
    "top5" : {
        "logo" : "Logo",
        "video" : "Video",
        "link" : "link"
    }
}


function setLinkBox(e)
{
    // You must add style. Here you put attributes to the tag! No valuesf for style!
    linkBox.setAttribute("display", "flex");
    linkBox.setAttribute("background-color", "yellow");
}


//event listeners//
anchors[0].addEventListener('mouseover', setLinkBox);
anchors[1].addEventListener('mouseover', setLinkBox);
anchors[2].addEventListener('mouseover', setLinkBox);
anchors[3].addEventListener('mouseover', setLinkBox);
anchors[4].addEventListener('mouseover', setLinkBox);
