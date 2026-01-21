import { createDiv, getCard } from './createElements.js';

window.createDiv = createDiv;
window.getCard = getCard;


const html = `
    <p> Você já estudou este assunto? </p>
    <button data-choice="yes">sim</button>
    <button data-choice="no">não</button>
`

const overlayDiv = document.querySelector('.overlay');

function cardListener(card, div) {
    card.addEventListener('click', (e) => {
        const choice = e.target.dataset.choice;

        if(!choice) return;

        const card = document.querySelector('.card');

        if(choice === 'no') overlayDiv.style.display = 'none';
        if(choice == 'yes') window.location.href = card.dataset.exerciciesUrl;

        localStorage.setItem('userChoice', choice);
    })
}

export function inicializeListener() {
    localStorage.clear()
    const choice = localStorage.getItem('userChoice');

    if(choice) {
        overlayDiv.style.display = 'none';
        return;
    };

    const div = window.createDiv(html);
    const card = window.getCard(div, '.card');

    cardListener(card, div);

}
