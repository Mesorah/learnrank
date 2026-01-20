function createElement() {
    const div = document.createElement('div');
    div.innerHTML = `
    <p> Você já estou esse assunto? </p>
    <button data-choice="yes">sim</button>
    <button data-choice="no">não</button>
    `;

    return div;
}

function getCard(div) {
    const card = document.querySelector('.card');

    card.appendChild(div);

    return card;
}

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

    const div = createElement();
    const card = getCard(div);

    cardListener(card, div);

}
