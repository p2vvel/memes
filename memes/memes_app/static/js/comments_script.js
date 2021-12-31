window.addEventListener("load", function () {


    let comments_section = document.querySelector("#comments_section");
    let meme_pk_value = document.querySelector("#meme_pk_value");
    let comments_buttons = document.querySelectorAll(".comments_button");
    let comments_spinner = document.querySelector("#comments_spinner");
    let comments_box = document.querySelector("#comments_box");
    // let comment_add_forms = document.querySelectorAll(".comments_add_form");


    comments_spinner.style.display = "none";


    //load comments at start
    load_comments(meme_pk_value.value, "new");

    //eventy podpiete pod przyciski do ladowania komentarzy
    comments_buttons.forEach(button => button.addEventListener("click", function () {
        load_comments(meme_pk_value.value, button.value);
    }));


    //event do dodawania komentarzy
    comments_section.addEventListener("submit", function (e) {
        if (e.target.classList.contains("comments_add_form")) {
            e.preventDefault();
            let form = e.target;
            let meme = meme_pk_value.value;
            let parent = form.querySelector("[name=parent]").value;
            let content = form.querySelector("[name=content]").value;
            add_comment(meme, parent, content);
        }
    });


    function load_comments(meme_pk, sort_style = "new") {
        let url = `/comments/meme/${meme_pk}/?sort=${sort_style}"`;
        let request = new Request(url, {headers: {"X-CSRFToken": csrf_token}});
        //turn on comments loading animation
        comments_spinner.style.display = "block";

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
                //turn off comments loading animation
                comments_spinner.style.display = "none";
                if (data.success) {
                    //clear old comments
                    comments_box.innerHTML = "";

                    //append comments to comments_box div
                    for (let comm of data.comments) {
                        let user_login = comm.fields.original_poster[0];
                        let user_avatar = comm.fields.original_poster[1] ? comm.fields.original_poster[1] : "/static/images/watermark.png";
                        let pk = comm.pk;
                        let content = comm.fields.content;
                        let karma = comm.fields.karma;

                        let date_created = new Date(comm.fields.date_created);
                        let date_printed = date_created.toLocaleString({
                            day: '2-digit', // numeric, 2-digit
                            year: 'numeric', // numeric, 2-digit
                            month: '2-digit', // numeric, 2-digit, long, short, narrow
                            hour: 'numeric', // numeric, 2-digit
                            minute: 'numeric', // numeric, 2-digit
                        });
                        let parent_margin = Boolean(comm.fields.parent_comment);    //indicates if comment should be displayed as reply (margin at left)

                        //TODO: podepnij guziki od oceny komentarza pod eventy zeby dzialalo
                        let comment_template = `<div class="card my-1 ${parent_margin ? "ms-5" : ""}" id=${`comment_${pk}`}>
                            <div class="card-body">
                                <div class="d-flex justify-content-start media position-relative">
                                    <img src="${user_avatar}" alt="${user_login} avatar" class="img-thumbnail img-fluid" style="max-height: 50px;">
                                    <div class="d-flex flex-column ms-2">
                                        <h6 class="card-title"><a href="/users/profile/${user_login}" class=" link-dark text-decoration-none">${user_login}</a></h6>
                                        <p class="card-subtitle mb-2 text-muted">${date_printed}</p>
                                    </div>
                                    <div class="d-flex justify-content-end flex-grow-1 align-items-center">
                                        <a class="btn btn-outline-link btn-sm me-2" type="button" data-bs-toggle="collapse" data-bs-target="#comment_${pk}_reply_box" aria-expanded="false" aria-controls="comment_${pk}_reply_box">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-reply-fill" viewBox="0 0 16 16">
                                                <path d="M5.921 11.9 1.353 8.62a.719.719 0 0 1 0-1.238L5.921 4.1A.716.716 0 0 1 7 4.719V6c1.5 0 6 0 7 8-2.5-4.5-7-4-7-4v1.281c0 .56-.606.898-1.079.62z"/>
                                            </svg>        
                                            Reply
                                        </a>

                                        <div class="btn-group" role="group" aria-label="Comment karma section">
                                            <button type="button" class="btn btn-outline-success btn-sm"><b>+</b></button>
                                            <button type="button" class="btn btn-outline-dark btn-sm" disabled><b>${karma}</b></button>
                                            <button type="button" class="btn btn-outline-danger btn-sm"><b>-</b></button>
                                        </div>
                                    </div>
                                </div>
                                <p class="card-text">${content}</p>
                            </div>
                            <div>
                            
                            
                            <div>
                                <div class="collapse" id="comment_${pk}_reply_box">
                                    <form method="POST" class="comments_add_form d-flex justify-content-between me-2 ms-5">
                                        <input type="hidden" name="parent" value="${pk}">
                                        <textarea name="content" maxlength="12000" placeholder="Comment..." class="flex-fill me-1 my-2" style="resize: vertical;"></textarea>
                                        <input type="submit" class="btn btn-outline-success ms-1 my-2">
                                    </form>
                                </div>
                            </div>

                            </div>
                        </div>`;

                        let new_comment = document.createElementFromString(comment_template, "text/html");
                        comments_box.appendChild(new_comment);
                    }

                } else {
                    throw Error("Data NOT OK");
                }
            })
            .catch(error => {
                console.log(error.message);
            });
    }


    function add_comment(meme_pk, parent_pk, content) {
        let url = (parent_pk === "" ? `/comments/meme/${meme_pk}/add/` : `/comments/comment/${parent_pk}/add/`);
        let request = new Request(url, {headers: {"X-CSRFToken": csrf_token}});
        let form_data = new FormData();
        form_data.append("content", content);

        fetch(request, {
            method: "POST",
            mode: "same-origin",
            body: form_data,
        })
            .then(response => {
                if (response.ok)
                    return response.json();
                else
                    throw Error(response.statusText);
            })
            .then(data => {
                if (data.success) {
                    load_comments(meme_pk, "new");
                } else {
                    throw Error("Data NOT OK");
                }
            })
            .catch(error => {
                console.log(error.message);
            });
    }


    //copied from: https://stackoverflow.com/a/45784892/16626390
    Document.prototype.createElementFromString = function (str) {
        const element = new DOMParser().parseFromString(str, 'text/html');
        return element.documentElement.querySelector('body').firstChild;
    };
});
