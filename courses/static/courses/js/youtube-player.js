let player;

function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        videoId: '6Gli-vT4SKI',
        events: {
            onStateChange: onPlayerStateChange
        }
    });
}

function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.ENDED) {
        const div = createElement();
        getCard(div);
    }
}

// function createElement() {
//     const div = document.createElement('div');
//     div.innerHTML = `
//     <a href="#">Resolver questões</a>
//     `;

//     return div;
// }

// function getCard(div) {
//     const card = document.querySelector('.exercicies');

//     card.appendChild(div);

//     return card;
// }