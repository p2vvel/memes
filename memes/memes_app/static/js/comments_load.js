window.addEventListener("load", function() {
    let comments_section = document.querySelector("#comments_section");
    let comments_button = document.querySelector("#comments_button");
    let comments_spinner = document.querySelector("#comments_spinner");
    
    comments_spinner.style.display = "none";
    comments_button.style.display = "block";

    comments_button.addEventListener("click", function(){
        let url = `/comments/meme/${comments_button.value}/`;
        let request = new Request(url, { headers: { "X-CSRFToken": csrf_token } });
        
        comments_spinner.style.display = "block";
        comments_button.style.display = "none";
        
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
            comments_spinner.style.display = "none";
            if (data.success){
                console.log(data);
                // karma_count.innerText = `${data.karma}`;
                // meme.classList.toggle("btn-success");
                // meme.classList.toggle("btn-outline-success");

            }
            else{
                console.log(data);
                throw Error("Data NOT OK");
            }
        })
        .catch(error => {
            console.log(error.message);
        });


    });


    });
