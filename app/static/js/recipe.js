window.onload = () => {
    const info = document.getElementsByClassName("product-info")
    for (let i = 0; i < info.length; i++) {
        info[i].value = parseFloat(info[i].value.replace(',', '.')).toFixed(2)
    }

    const steps = document.getElementById("stepsContainer")
    for (var i = 0; i < steps.children.length; i++) {
        steps.children[i].getElementsByClassName("step-title")[0].innerHTML = "Step " + (i + 1)
    }

    doneBtn.onclick = () => {
        window.location.replace('/create_recipe/' + document.getElementById("recipe").getAttribute("data-id"))
    }

    likeBtn.onclick = likeBtnClicked
}


async function likeBtnClicked() {
    let response = await fetch('/api/like_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        
        body: JSON.stringify({
            'user': document.getElementById("likeBtn").getAttribute("data-user"),
            'recipe': document.getElementById("likeBtn").getAttribute("data-recipe")
        })
    });

    if (response.ok) {
        data = await response.json()
        if (data['success'] == true) {
            location.reload()
        } else {
            console.log(data['message'])
        }
    } 
}
