window.addEventListener("load", function () {
    let memesArray = document.querySelectorAll(".karma_button");

    // for (let i = 0; i < memes.length; i++)   
    memesArray.forEach(meme => meme.addEventListener("click", () => {
        let karma_count = meme.querySelector(".karma_count");
        let url = `/meme/${meme.value}/karma/`;
        let request = new Request(url, { headers: { "X-CSRFToken": csrf_token } });
        
        
        fetch(request, {
            method: "POST",
            mode: "same-origin"
        })
        .then(response => {
            if (response.ok)
                return response.json();
            else
                throw Error(response.statusText);
        })
        .then(data => {
            if (data.success){
                karma_count.innerText = `${data.karma}`;
                meme.classList.toggle("btn-success");
                meme.classList.toggle("btn-outline-success");

            }
            else
                throw Error("Data NOT OK");
        })
        .catch(error => {
            console.log(error.message);
        });
    }));


});