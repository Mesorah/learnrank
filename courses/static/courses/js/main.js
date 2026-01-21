import { createDiv, getCard } from './createElements.js';

window.createDiv = createDiv;
window.getCard = getCard;

const html = `
    <p> Você já estou esse assunto? </p>
    <button data-choice="yes">sim</button>
    <button data-choice="no">não</button>
`

function cardListener(card, div) {
    card.addEventListener('click', (e) => {
        const choice = e.target.dataset.choice;

        if(!choice) return;

        if(choice === 'no') div.style.display = 'none';

        localStorage.setItem('userChoice', choice);
    })
}

export function inicializeListener() {
    const choice = localStorage.getItem('userChoice');

    if(choice) return;

    const div = window.createDiv(html);
    const card = window.getCard(div, '.card');

    cardListener(card, div);

}
