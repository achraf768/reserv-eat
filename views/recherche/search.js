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