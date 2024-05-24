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

// Pour apparition / disparition du contenu dans la barre de recherche quand "focused"

const srch = document.getElementById('search-bar');
const svg = document.getElementById('search-svg')

srch.addEventListener('focus', () => {
    svg.style.display = 'none'
    srch.setAttribute('data-placeholder', srch.getAttribute('placeholder'));
    srch.setAttribute('placeholder', '');
});

srch.addEventListener('blur', () => {
    svg.style.display = 'block'
    srch.setAttribute('placeholder', srch.getAttribute('data-placeholder'));
});