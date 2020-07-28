function alertDiv(message, classes) {
    let template = document.createElement("template");
    let html = `
    <div class="alert ${classes}">
        ${message}
        <button type="button" 
                class="close" 
                data-dismiss="alert"
                aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    `
    html = html.trim();
    template.innerHTML = html;
    return template.content.firstChild;
}

async function castVote(voteForm) {
    let data = {
        "question_id": voteForm["question_id"].value,
        "direction": voteForm["direction"].value,
    }

    fetch(voteForm.action, {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": voteForm["csrfmiddlewaretoken"].value,
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify(data)
    }).then(response => {
        return response.json()
    }).then(responseJSON => {
        if (responseJSON.error) {
            voteForm.parent.insertBefore(alertDiv(responseJSON.error, "alert-danger"))
        } else {

        }
    })
}
const voteForms = document.getElementsByClassName("vote-form");

for (let element of voteForms ){
    element.addEventListener("submit", function(event) {
        event.preventDefault();
        castVote(element);
    });
}
