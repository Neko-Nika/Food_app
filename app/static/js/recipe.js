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
}

