function createElement() {
    const div = document.createElement('div');
    div.innerHTML = `
    <p> Você já estou esse assunto? </p>
    <button>sim</button>
    <button>não</button>
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
        const text = e.target.textContent;

        if(text === 'não') div.style.display = 'none';
    })
}

export function inicializeListener() {
    const div = createElement();
    const card = getCard(div);

    cardListener(card, div);

}