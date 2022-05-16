const DEFAULT = "default";

nameImageMap = {
    "globo": "imgs/channels/globo.jpg",
    "globo news": "imgs/channels/globonews.jpeg",
    "multishow": "imgs/channels/multishow.jpg",
    "cnn": "imgs/channels/cnn.jpg",
    "cnn esp": "imgs/channels/cnn_espanol.jpg",
    "sportv": "imgs/channels/sportv.jpg",
    "sportv2": "imgs/channels/sportv2.jpg",
    "globo play": "imgs/streaming/globo_play.jpg",
    "disney plus": "imgs/streaming/disneyplus.jpg",
    "netflix": "imgs/streaming/netflixlogo.jpg",
    "prime": "imgs/streaming/prime.jpg",
    "youtube": "imgs/streaming/youtube.jpg"
};


function title(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


function createCard(img, link) {
    let cdiv = document.createElement('div');
    cdiv.className = "column";
    
    let card = document.createElement('div');
    card.className = "card div-with-bg round-large";
    card.style = `background-image: url('${img}')`;

    cdiv.appendChild(card);
    return cdiv;
}


function createDivCards(data, type, user=DEFAULT) {
    let live = document.getElementById(type);
    data[user][type].forEach(channelName => {
        let channelUrl = nameImageMap[channelName];
        live.appendChild(createCard(channelUrl));
    });
}


function queryUrl() {
    let searchParams = new URLSearchParams(window.location.search);
    return searchParams.has('user') ? searchParams.get('user') : DEFAULT;
}


function main(user) {
    user = queryUrl();
    user = user.replace(/"/g, "");
    if (!data[user]) user = DEFAULT;

    dataDiv = document.getElementById("data");
    data[user]["order"].forEach(type => {
        // create title
        let h3 = document.createElement("h3");
        h3.textContent = title(type);
        dataDiv.appendChild(h3);

        // create div to hold contents
        let div = document.createElement("div");
        div.className = "row";
        div.id = type;
        dataDiv.appendChild(div);

        createDivCards(data, type, user);
    });
}



data = JSON.parse(data);
main();
