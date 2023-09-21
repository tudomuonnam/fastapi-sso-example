
//java script for menu user in nav

const user_btn = document.getElementById("user_btn");
const menu = document.getElementById("user_dropdown");


user_btn.addEventListener("click", () =>{
    menu.toggleAttribute("hidden");
});

// menu.addEventListener("blur", () =>{
//     menu.setAttribute("hidden");


function userMenuLostFocus(){
    menu.setAttribute("hidden");
}