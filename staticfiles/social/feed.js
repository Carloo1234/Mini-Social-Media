const comment_btn = document.querySelector(".comment-button")


function handleLike(btn){
    const postId = btn.dataset.postId
    fetch(`/like/${postId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
            updateLikeUI(btn, data.liked, data.likes_count
        )})
}



function updateLikeUI(btn, liked, likes_count){
    icon = btn.querySelector("i")
    if (liked){
        icon.classList.remove("fa-regular")
        icon.classList.add("fa-solid")
    }
    else{
        icon.classList.remove("fa-solid")
        icon.classList.add("fa-regular")
    }
    btn.nextElementSibling.textContent = likes_count
}


function getCSRFToken(){
    return document.cookie.split("; ")
    .find(cookie => cookie.startsWith("csrftoken="))
    ?.split("=")[1];
}
