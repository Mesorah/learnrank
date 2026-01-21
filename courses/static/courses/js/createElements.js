export function createDiv(html) {
    const div = document.createElement('div');
    div.innerHTML = html;

    return div;
}

export function getCard(div, id) {
    const card = document.querySelector(id);

    card.appendChild(div);

    return card;
}