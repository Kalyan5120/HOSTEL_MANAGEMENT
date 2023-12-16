let ol = document.getElementById("menu")
console.log(ol);
// console.log(ol[0].children);
// console.log(ol[0].children[2]);

ol.onclick = function(){
    let div = document.getElementById("ull")
    console.log(div[0]);
    let display =div[0].classList.toggle("none")
    if (display){
        div[0].style.display = "block"
    }
    else{
        div[0].style.display = "none"
    }
}