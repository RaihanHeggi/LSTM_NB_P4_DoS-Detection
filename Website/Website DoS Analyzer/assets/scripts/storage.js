const CACHE_KEY = "history";

function checkForStorage() {
    return typeof (Storage) !== "undefined";
}
function showComments(data) {
    if (checkForStorage()) {
        let historyData = null, history = [];
        historyData = localStorage.getItem(CACHE_KEY) == null ? [] : JSON.parse(localStorage.getItem(CACHE_KEY));
        historyData.unshift(data);
        for (const iterator of historyData)
            if (iterator != null)
                history.unshift(iterator);
        localStorage.setItem(CACHE_KEY, JSON.stringify(history));
    }
}
function showHistory() {
    return checkForStorage() ? JSON.parse(localStorage.getItem(CACHE_KEY)) || [] : [];
}
function renderComments() {
    const fullData = showHistory();
    console.log(fullData);
    let commentList = document.querySelector('.kolom-komentar-card');
    commentList.innerHTML = "";
    for (let history of fullData) {
        let container = document.createElement('div');
        container.className = "kolom-komentar-card";
        container.innerHTML = '<img class="avatar" src="assets/image/avata.png" alt="avatar">';
        container.innerHTML += '<h3 class="name">' + history.username + "</h3>";
        container.innerHTML += '<p class="date">' + history.date + "</p>";
        container.innerHTML += '<p class="comment">' + history.comments + "</p>";
        container.innerHTML += "<br>";
        
        commentList.appendChild(container);
    }
    document.querySelector("#jumkomentar").innerText = fullData.length;
}

renderComments();