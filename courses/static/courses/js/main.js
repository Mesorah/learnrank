import { createDiv, getCard } from './createElements.js';

window.createDiv = createDiv;
window.getCard = getCard;

const html = `
    <p> Você já estudou este assunto? </p>
    <button data-choice="yes">sim</button>
    <button data-choice="no">não</button>
`

function cardListener(card, div) {
    card.addEventListener('click', (e) => {
        const choice = e.target.dataset.choice;

        if(!choice) return;

        const cardDiv = div.parentElement;
        const overlayDiv = cardDiv.parentElement;

        if(choice === 'no') overlayDiv.style.display = 'none';

        localStorage.setItem('userChoice', choice);
    })
}

export function inicializeListener() {
    localStorage.removeItem('userChoice')
    const choice = localStorage.getItem('userChoice');

    if(choice) return;

    const div = window.createDiv(html);
    const card = window.getCard(div, '.card');

    cardListener(card, div);

}
