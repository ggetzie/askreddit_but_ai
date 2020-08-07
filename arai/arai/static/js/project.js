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
        method: "POST",
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
            let question = voteForm.parentElement.parentElement;
            let voteState = responseJSON.vote_state;
            if (voteState === 1) {
                question.classList.remove("neutral");
                question.classList.remove("downvoted");
                question.classList.add("upvoted");
            } else if (voteState === 0) {
                question.classList.remove("upvoted");
                question.classList.remove("downvoted");
                question.classList.add("neutral");
            } else if (voteState === -1) {
                question.classList.remove("neutral");
                question.classList.remove("upvoted");
                question.classList.add("downvoted");
            }
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

function load_vote_state() {
    if (typeof(vote_states) === "undefined") {
        return null;
    }
    for (const v_id in vote_states) {
        let q_id = `question${v_id.slice(v_id.search(/\d+$/))}`;
        let question = document.getElementById(q_id);
        if (question) {
            let vs = vote_states[v_id];
            if (vs === 1) {
                question.classList.remove("neutral");
                question.classList.remove("downvoted");
                question.classList.add("upvoted");
            } else if (vs === -1) {
                question.classList.remove("neutral");
                question.classList.remove("upvoted");
                question.classList.add("downvoted");
            } else {
                question.classList.remove("upvoted");
                question.classList.remove("downvoted");
                question.classList.add("neutral");
            }

        }
        
    }
}

window.onload = load_vote_state;
