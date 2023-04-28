window.onload = () => {
    doneBtn.onclick = createRecipe

    const products = document.getElementById("productsContainer").children
    for (let i = 0; i < products.length; i++) {
        products[i].id = "product_" + i
    } 

    const info = document.getElementsByClassName("product-info")
    for (let i = 0; i < info.length; i++) {
        info[i].value = parseFloat(info[i].value.replace(',', '.')).toFixed(2)
    }

    const steps = document.getElementById("stepsContainer")
    for (var i = 0; i < steps.children.length; i++) {
        steps.children[i].getElementsByClassName("step-title")[0].innerHTML = "Step " + (i + 1)
        steps.children[i].id = "step_" + i
    }
}

function removeProduct(element) {
    if (document.getElementById("productsContainer").children.length === 1) {
        var pr = document.getElementById("productsContainer").firstElementChild
        pr.id = "product_0"
        clearInputs(pr)
    } else {
        element.remove()
    }
    updateTotal()
}

function showInformation(element) {
    var info = element.getElementsByClassName("product-info")
    var list = document.getElementById("datalistOptions")
    var amount = parseInt(element.getElementsByClassName("amount-input")[0].value)
    var value = element.getElementsByClassName("product-input")[0].value

    if (value === "") {
        info[0].value = 0.0
        info[1].value = 0.0
        info[2].value = 0.0
        info[3].value = 0.0
    }

    for (i = 0; i < list.options.length; i++) {
        if (list.options[i].value === value) {
            info[0].value = (parseFloat(list.options[i].getAttribute("data-proteins").replace(',', '.')) * amount).toFixed(2)
            info[1].value = (parseFloat(list.options[i].getAttribute("data-fats").replace(',', '.')) * amount).toFixed(2)
            info[2].value = (parseFloat(list.options[i].getAttribute("data-carbohydrates").replace(',', '.'))* amount).toFixed(2)
            info[3].value = parseFloat(list.options[i].getAttribute("data-calories").replace(',', '.')) * amount
        }
    }
    
    updateTotal()
}

function addProduct() {
    var product = document.getElementById("productsContainer").firstElementChild.cloneNode(true)
    clearInputs(product)
    product.id = "product_" + document.getElementById("productsContainer").children.length
    document.getElementById("productsContainer").appendChild(product)
}

function clearInputs(element) {
    tags = element.getElementsByTagName("input")
    tags[0].value = ""
    tags[1].value = "1"
    for (var i = 2; i < tags.length; i++) {
        tags[i].value = "0.00"
    }
}

function updateTotal() {
    var proteins = 0
    var fats = 0
    var carbohydrates = 0
    var calories = 0

    const products = document.getElementById("productsContainer").children
    for (var i = 0; i < products.length; i++) {
        var elements = products[i].getElementsByClassName("product-info")
        
        if (elements[0].value != "")
            proteins += parseFloat(elements[0].value)
        if (elements[1].value != "")
            fats += parseFloat(elements[1].value)
        if (elements[2].value != "")
            carbohydrates += parseFloat(elements[2].value)
        if (elements[3].value != "")
            calories += parseFloat(elements[3].value)
    }

    document.getElementById("proteinsTotal").value = proteins.toFixed(2)
    document.getElementById("fatsTotal").value = fats.toFixed(2)
    document.getElementById("carbohydratesTotal").value = carbohydrates.toFixed(2)
    document.getElementById("caloriesTotal").value = calories.toFixed(2)
}

function addStep() {
    var step = document.getElementById("stepsContainer").firstElementChild.cloneNode(true)
    step.getElementsByTagName("input")[0].value = ""
    step.getElementsByTagName("textarea")[0].value = ""

    step.id = "step_" + document.getElementById("stepsContainer").children.length
    step.getElementsByClassName("step-title")[0].innerHTML = "Step " + (document.getElementById("stepsContainer").children.length + 1)
    document.getElementById("stepsContainer").appendChild(step)
}

function removeStep(element) {
    var steps = document.getElementById("stepsContainer")

    if (steps.children.length === 1) {
        var pr = document.getElementById("stepsContainer").firstElementChild
        pr.id = "step_0"
        pr.getElementsByTagName("input")[0].value = ""
        pr.getElementsByTagName("textarea")[0].value = ""

    } else {
        element.remove()
    }

    for (var i = 0; i < steps.children.length; i++) {
        steps.children[i].getElementsByClassName("step-title")[0].innerHTML = "Step " + (i + 1)
    }
}

async function createRecipe(event) {
    document.getElementById("error").hidden = true
    document.getElementById("error").innerHTML = ""

    if (!create_recipe.reportValidity()){
        document.getElementById("error").hidden = false
        document.getElementById("error").innerHTML = "Не все обязательные поля заполнены"
        return
    }

    const formData = new FormData();
    formData.append("image", document.getElementById("imgInput").files[0])

    info = {'title': titleInput.value, 'total_proteins': proteinsTotal.value, 
            'total_fats': fatsTotal.value, 'total_carbohydrates': carbohydratesTotal.value,
            'total_calories': caloriesTotal.value
    }

    const products = document.getElementById("productsContainer").children
    for (var i = 0; i < products.length; i++) {
        info[products[i].id] = products[i].getElementsByClassName("product-input")[0].value
        info['amount_' + products[i].id] = products[i].getElementsByClassName("amount-input")[0].value
    }
    
    const steps = document.getElementById("stepsContainer").children
    for (var i = 0; i < steps.length; i++) {
        info[steps[i].id] = steps[i].getElementsByClassName("step-input")[0].value
        info['description_' + steps[i].id] = steps[i].getElementsByClassName("description-input")[0].value
    }

    for ( var key in info ) {
        formData.append(key, info[key]);
    }

    var url = '/api/create_new_recipe'
    const status = parseInt(document.getElementById("titleInput").getAttribute("data-status"))
    if (status === 2) {
        url = '/api/edit_recipe/' + document.getElementById("create_recipe").getAttribute("data-id")
    } 

    let response = await fetch(url, {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        data = await response.json()
        if (data['success'] == true) {
            window.location.replace("/recipes");
        } else {
            console.log(data['message'])
            document.getElementById("error").hidden = false
            document.getElementById("error").innerHTML = data['message']
        }
    } 
}

function showPreview(element) {
    var file = document.getElementById("imgInput").files[0]
    if (file) {
        var fr = new FileReader();
        fr.onload = function () {
            document.getElementById("previewImg").src = fr.result;
            document.getElementById("previewContainer").hidden = false
        }
        fr.readAsDataURL(file);
    } else {
        document.getElementById("previewImg").setAttribute("src", document.getElementById("previewImg").getAttribute("data-original"))
        document.getElementById("previewContainer").hidden = true
    }
}
