const navbar = document.querySelector(".custom-navbar");

console.log(navbar);

window.addEventListener("scroll", function () {
    console.log("scrolling");
});
let lastScroll = 0;

const navbar = document.querySelector(".custom-navbar");

window.addEventListener("scroll", () => {

    let current = window.pageYOffset;

    if (current <= 0) {
        navbar.classList.remove("hide");
        return;
    }

    if (current > lastScroll) {
        navbar.classList.add("hide");
    } else {
        navbar.classList.remove("hide");
    }

    lastScroll = current;
});


// window.addEventListener("scroll", function(){

//     const navbar = document.querySelector(".custom-navbar");

//     if(window.scrollY > 50){
//         navbar.classList.add("scrolled");
//     }else{
//         navbar.classList.remove("scrolled");
//     }

// });

// const navbar = document.querySelector(".custom-navbar");

// let lastScroll = 0;

// // Hide while scrolling down
// window.addEventListener("scroll", () => {

//     const current = window.pageYOffset;

//     if(current > lastScroll && current > 100){

//         navbar.classList.add("hide");
//         navbar.classList.remove("show");

//     }else{

//         navbar.classList.remove("hide");
//         navbar.classList.add("show");

//     }

//     lastScroll = current;

// });

// // Show when mouse reaches the top of the page
// document.addEventListener("mousemove", function(e){

//     if(e.clientY < 15){

//         navbar.classList.remove("hide");
//         navbar.classList.add("show");

//     }

// });

// console.log("main.js loaded");