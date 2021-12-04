window.addEventListener("load", function () {
    //copied from: https://stackoverflow.com/a/45784892/16626390
    Document.prototype.createElementFromString = function (str) {
        const element = new DOMParser().parseFromString(str, 'text/html');
        const child = element.documentElement.querySelector('body').firstChild;
        return child;
    };


    let comments_section = document.querySelector("#comments_section");
    let comments_button = document.querySelector("#comments_button");
    let comments_spinner = document.querySelector("#comments_spinner");
    let comments_box = document.querySelector("#comments_box");

    comments_spinner.style.display = "none";
    comments_button.style.display = "block";

    comments_button.addEventListener("click", function () {
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
                console.log(data)
                comments_spinner.style.display = "none";
                if (data.success) {
                    //append comments to comments_box div
                    for (let comm of data.comments) {
                        let user = comm.fields.original_poster;
                        let pk = comm.fields.pk;
                        let content = comm.fields.content;
                        let date_created = new Date(comm.fields.date_created);
                        let date_printed = date_created.toLocaleString({
                            day: '2-digit', // numeric, 2-digit
                            year: 'numeric', // numeric, 2-digit
                            month: '2-digit', // numeric, 2-digit, long, short, narrow
                            hour: 'numeric', // numeric, 2-digit
                            minute: 'numeric', // numeric, 2-digit
                        });

                        let comment_template = `<div class="card" style="width: 18rem;">
                        <div class="card-body">
                          <h6 class="card-title">${user}</h6>
                          <p class="card-subtitle mb-2 text-muted">${date_printed}</p>
                          <p class="card-text">${content}</p>
                        </div>
                      </div>`


                        let new_comment = document.createElementFromString(comment_template, "text/html");
                        comments_box.appendChild(new_comment);

                    }

                }
                else {
                    throw Error("Data NOT OK");
                }
            })
            .catch(error => {
                console.log(error.message);
            });


    });


});
