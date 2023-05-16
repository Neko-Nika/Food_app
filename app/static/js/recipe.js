window.onload = () => {
    const info = document.getElementsByClassName("product-info")
    for (let i = 0; i < info.length; i++) {
        info[i].value = parseFloat(info[i].value.replace(',', '.')).toFixed(2)
    }

    const steps = document.getElementById("stepsContainer")
    for (var i = 0; i < steps.children.length; i++) {
        steps.children[i].getElementsByClassName("step-title")[0].innerHTML = "Step " + (i + 1)
    }

    setupParameters()

    doneBtn.onclick = () => {
        window.location.replace('/create_recipe/' + document.getElementById("recipe").getAttribute("data-id"))
    }

}


function setupParameters() {
    var products = document.getElementById("productsContainer").children

    for (let i = 0; i < products.length; i++) {
        var amount = parseInt(products[i].getElementsByClassName("amount-input")[0].value)
        var info = products[i].getElementsByClassName("product-info")

        info[0].value = (parseFloat(info[0].value.replace(',', '.')) / 100 * amount).toFixed(2)
        info[1].value = (parseFloat(info[1].value.replace(',', '.')) / 100 * amount).toFixed(2)
        info[2].value = (parseFloat(info[2].value.replace(',', '.')) / 100 * amount).toFixed(2)
        info[3].value = Math.round(parseInt(info[3].value.replace(',', '.')) / 100 * amount)
    }
   
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

async function delBtnClicked() {
    console.log(1)
    let response = await fetch('/api/delete_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        
        body: JSON.stringify({
            'recipe': document.getElementById("delBtn").getAttribute("data-recipe")
        })
    });

    if (response.ok) {
        data = await response.json()
        if (data['success'] == true) {
            window.location.replace("/recipes")
        } else {
            console.log(data['message'])
        }
    }
}
