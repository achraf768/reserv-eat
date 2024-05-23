document.addEventListener('input', handicap);

const handicapSelector = document.getElementById("handicap")
const selectField = document.getElementById("handicap-type")

function handicap (){
    if(handicapSelector.checked){
        selectField.style.display = "block"
    }else if(!handicapSelector.checked){
        selectField.style.display = "none"
    }
};