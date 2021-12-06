window.addEventListener("load", function () {



    let comments_section = document.querySelector("#comments_section");
    let meme_pk_value = document.querySelector("#meme_pk_value");
    let comments_buttons = document.querySelectorAll(".comments_button");
    let comments_spinner = document.querySelector("#comments_spinner");
    let comments_box = document.querySelector("#comments_box");
    let comment_add_forms = document.querySelectorAll(".comments_add_form");


    comments_spinner.style.display = "none";


    //load comments at start
    load_comments(meme_pk_value.value, "new");
    


    comments_buttons.forEach(button => button.addEventListener("click", function () {
        load_comments(meme_pk_value.value, button.value);
    }));


    comment_add_forms.forEach(form => form.addEventListener("submit", function (e) {
        e.preventDefault();
        let meme = meme_pk_value.value;
        let parent = form.querySelector("[name=parent]").value;
        let content = form.querySelector("[name=content]").value;
        add_comment(meme, parent, content);
    }));



    function load_comments(meme_pk, sort_style = "new") {
        let url = `/comments/meme/${meme_pk}/?sort=${sort_style}"`;
        let request = new Request(url, { headers: { "X-CSRFToken": csrf_token } });
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
                        let date_created = new Date(comm.fields.date_created);
                        let date_printed = date_created.toLocaleString({
                            day: '2-digit', // numeric, 2-digit
                            year: 'numeric', // numeric, 2-digit
                            month: '2-digit', // numeric, 2-digit, long, short, narrow
                            hour: 'numeric', // numeric, 2-digit
                            minute: 'numeric', // numeric, 2-digit
                        });
                        let parent_margin = Boolean(comm.fields.parent_comment);    //indicates if comment should be displayed as reply (margin at left) 

                        let comment_template = `<div class="card my-1 ${parent_margin ? "ms-5" : ""}" id=${`comment_${pk}`}>
                            <div class="card-body">
                                <div class="d-flex justify-content-start media position-relative">
                                    <img src="${user_avatar}" alt="${user_login} avatar" class="img-thumbnail img-fluid" style="max-height: 50px;">
                                    <div class="d-flex flex-column ms-2">
                                        <h6 class="card-title"><a href="/users/profile/${user_login}" class=" link-dark text-decoration-none">${user_login}</a></h6>
                                        <p class="card-subtitle mb-2 text-muted">${date_printed}</p>
                                    </div>
                                    <div class="d-flex justify-content-end flex-grow-1">
                                        <a class="link-primary text-decoration-none" type="button" data-bs-toggle="collapse" data-bs-target="#comment_${pk}_reply_box" aria-expanded="false" aria-controls="comment_${pk}_reply_box">
                                            Reply
                                        </a>
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
                    };

                    //add events to new reply forms (added after load, so initial event adding doesnt affected them)
                    document.querySelectorAll(".comments_add_form").forEach(form => form.addEventListener("submit", function (e) {
                        console.log("DODAJEM hehe");
                        e.preventDefault();
                        let meme = meme_pk_value.value;
                        let parent = form.querySelector("[name=parent]").value;
                        let content = form.querySelector("[name=content]").value;
                        add_comment(meme, parent, content);
                    }));
                }
                else {
                    throw Error("Data NOT OK");
                }
            })
            .catch(error => {
                console.log(error.message);
            });
    };



    function add_comment(meme_pk, parent_pk, content) {
        let url = (parent_pk == "" ? `/comments/meme/${meme_pk}/add/` : `/comments/comment/${parent_pk}/add/`);
        console.log(url);
        let request = new Request(url, { headers: { "X-CSRFToken": csrf_token } });
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
                console.log(data)
                if (data.success) {
                    console.log("Success");
                    load_comments(meme_pk, "new");
                }
                else {
                    throw Error("Data NOT OK");
                }
            })
            .catch(error => {
                console.log(error.message);
            });
    };



    //copied from: https://stackoverflow.com/a/45784892/16626390
    Document.prototype.createElementFromString = function (str) {
        const element = new DOMParser().parseFromString(str, 'text/html');
        const child = element.documentElement.querySelector('body').firstChild;
        return child;
    };
});
