const html = `
    <a href="#">Resolver questões</a>
`

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
        const div = window.createDiv(html);
        window.getCard(div, '.exercicies');
    }
}
