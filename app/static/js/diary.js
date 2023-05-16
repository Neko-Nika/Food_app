window.onload = () => {
    if (document.getElementById("extra_info").getAttribute("data-obj") === "1") {
        document.getElementById("waterInput").value = parseFloat(document.getElementById("waterTotal").value.replace(',', '.')).toFixed(2)
        document.getElementById("doneBtn").innerText = "Apply changes"
        updateTotal()
    } 
    document.getElementById("date").min = new Date().toLocaleDateString('fr-ca')

    document.getElementById("addRecipeModal").addEventListener("show.bs.modal", function (event) {
        var category = event.relatedTarget.getAttribute("data-bs-category")
        document.getElementById("extra_info").setAttribute("data-category", category)
        if (category !== "water-tracker")
            document.getElementById("addRecipeModalLabel").textContent = "Add meals to your " + category
        else
            document.getElementById("addRecipeModalLabel").textContent = "Add information to your " + category
    })

    const info = document.getElementsByClassName("product-info")
    for (let i = 0; i < info.length; i++) {
        info[i].value = parseFloat(info[i].value.replace(',', '.')).toFixed(2)
    }
    
}

function nextDay() {
    var elem = document.getElementById("date")
    var tommorow = new Date(elem.valueAsDate)
    tommorow.setDate(tommorow.getDate() + 1)
    elem.valueAsDate = tommorow

    redirectToDate()
}

function prevDay() {
    var elem = document.getElementById("date")
    if (elem.value !== elem.min) {
        var yesterday = new Date(elem.valueAsDate)
        yesterday.setDate(yesterday.getDate() - 1)
        elem.valueAsDate = yesterday
    }

    redirectToDate()
}

function setupParameters() {
    const list = document.getElementById("dataListRecipes")
    const value = document.getElementById("recipeInput").value

    for (let i = 0; i < list.options.length; i++) {
        if (list.options[i].value === value) {
            document.getElementById("amountInput").value = parseInt(list.options[i].getAttribute("data-grams"))
            document.getElementById("proteins").value = parseFloat(list.options[i].getAttribute("data-proteins").replace(',', '.')).toFixed(2)
            document.getElementById("fats").value = parseFloat(list.options[i].getAttribute("data-fats").replace(',', '.')).toFixed(2)
            document.getElementById("carbohydrates").value = parseFloat(list.options[i].getAttribute("data-carbohydrates").replace(',', '.')).toFixed(2)
            document.getElementById("calories").value = parseInt(list.options[i].getAttribute("data-calories").replace(',', '.')).toFixed(2)

            document.getElementById("recipeImage").hidden = false
            document.getElementById("recipeImage").src = list.options[i].getAttribute("data-img")
            document.getElementById("amountInput").disabled = false

            const amount = document.getElementById("amountInput").value
            const extra = document.getElementById("extra_info")
            extra.setAttribute("data-id", list.options[i].getAttribute("data-id"))
            extra.setAttribute("data-protein_per_gram",  document.getElementById("proteins").value / amount)
            extra.setAttribute("data-fats_per_gram",  document.getElementById("fats").value / amount)
            extra.setAttribute("data-carbohydrates_per_gram",  document.getElementById("carbohydrates").value / amount)
            extra.setAttribute("data-calories_per_gram",  document.getElementById("calories").value / amount)

            return;
        }
    }

    document.getElementById("recipeImage").hidden = true
    document.getElementById("recipeImage").src = ""
    document.getElementById("amountInput").disabled = true

    clearForRecipes()
}

function setupParametersProduct() {
    const list = document.getElementById("dataListProducts")
    const value = document.getElementById("productInput").value

    for (let i = 0; i < list.options.length; i++) {
        if (list.options[i].value === value) {
            document.getElementById("amountInputProduct").value = parseInt("100")
            document.getElementById("proteins").value = parseFloat(list.options[i].getAttribute("data-proteins").replace(',', '.')).toFixed(2)
            document.getElementById("fats").value = parseFloat(list.options[i].getAttribute("data-fats").replace(',', '.')).toFixed(2)
            document.getElementById("carbohydrates").value = parseFloat(list.options[i].getAttribute("data-carbohydrates").replace(',', '.')).toFixed(2)
            document.getElementById("calories").value = parseInt(list.options[i].getAttribute("data-calories").replace(',', '.')).toFixed(2)

            document.getElementById("amountInputProduct").disabled = false

            const amount = document.getElementById("amountInputProduct").value
            const extra = document.getElementById("extra_info")
            extra.setAttribute("data-protein_per_gram",  document.getElementById("proteins").value / amount)
            extra.setAttribute("data-fats_per_gram",  document.getElementById("fats").value / amount)
            extra.setAttribute("data-carbohydrates_per_gram",  document.getElementById("carbohydrates").value / amount)
            extra.setAttribute("data-calories_per_gram",  document.getElementById("calories").value / amount)

            return;
        }
    }

    document.getElementById("amountInputProduct").disabled = true
    clearForProducts()
}

function filterRecipes(value) {
    document.getElementById("recipeInput").setAttribute('list', value)
}

function clearForRecipes() {
    document.getElementById("recipeInput").value = ""
    document.getElementById("amountInput").value = ""
    document.getElementById("recipeImage").hidden = true
    document.getElementById("recipeImage").src = ""
    document.getElementById("proteins").value = "0.00"
    document.getElementById("fats").value = "0.00"
    document.getElementById("carbohydrates").value = "0.00"
    document.getElementById("calories").value = "0.00"
}

function clearForProducts() {
    document.getElementById("productInput").value = ""
    document.getElementById("amountInputProduct").value = ""
    document.getElementById("proteins").value = "0.00"
    document.getElementById("fats").value = "0.00"
    document.getElementById("carbohydrates").value = "0.00"
    document.getElementById("calories").value = "0.00"
}

function clearAll() {
    clearForProducts()
    clearForRecipes()
}

function updateParameters(value) {
    const extra = document.getElementById("extra_info")
    let val = parseInt(value)

    document.getElementById("proteins").value = (val * parseFloat(extra.getAttribute("data-protein_per_gram"))).toFixed(2)
    document.getElementById("fats").value = (val * parseFloat(extra.getAttribute("data-fats_per_gram"))).toFixed(2)
    document.getElementById("carbohydrates").value = (val * parseFloat(extra.getAttribute("data-carbohydrates_per_gram"))).toFixed(2)
    document.getElementById("calories").value = parseInt((val * parseFloat(extra.getAttribute("data-calories_per_gram"))).toFixed(2))
}

function saveBtnClicked() {
    var name = ""
    var grams = ""
    var category = document.getElementById("extra_info").getAttribute("data-category")
    var container = document.getElementById(category + "Collapsed")
    var node = document.getElementById("copy").cloneNode(true)

    node.id = `${category}_${container.children.length}`

    if (document.getElementById("recipeInput").value !== "") {
        name = document.getElementById("recipeInput").value.split(' by ')[0]
        grams = document.getElementById("amountInput").value
        node.querySelector("#copyname").href = `/recipe/${document.getElementById("extra_info").getAttribute("data-id")}`
        node.querySelector("#copyname").innerText = "Recipe"
        node.setAttribute("data-id", document.getElementById("extra_info").getAttribute("data-id"))
    } else {
        name = document.getElementById("productInput").value
        grams = document.getElementById("amountInputProduct").value 
        node.querySelector("#copyname").innerText = "Product"
        node.querySelector("#copyname").removeAttribute("href")
    }

    node.querySelector("#copyinputname").value = name
    node.querySelector("#copygrams").value = grams
    node.querySelector("#copyproteins").value = document.getElementById("proteins").value
    node.querySelector("#copyfats").value = document.getElementById("fats").value
    node.querySelector("#copycarbohydrates").value = document.getElementById("carbohydrates").value
    node.querySelector("#copycalories").value = document.getElementById("calories").value

    node.hidden = false
    container.appendChild(node)

    updateTotal()
}

function updateTotal() {
    var proteins = 0
    var fats = 0
    var carbohydrates = 0
    var calories = 0
    var water = 0

    var categories = document.getElementsByClassName("category")
    for (let i = 0; i < categories.length; i++) {
        var menu = categories[i].getElementsByClassName("collapse")[0].children
        var local_calories = 0
        
        for (let j = 0; j < menu.length; j++) {
            var info = menu[j].getElementsByClassName("product-info")

            if (info[0].value != "")
                proteins += parseFloat(info[0].value)
            if (info[1].value != "")
                fats += parseFloat(info[1].value)
            if (info[2].value != "")
                carbohydrates += parseFloat(info[2].value)
            if (info[3].value != "") {
                calories += parseInt(info[3].value)
                local_calories += parseInt(info[3].value)
            }
        }

        var name = categories[i].getElementsByClassName("collapse-btn")[0].innerText.split(' - ')[0]
        if (local_calories > 0) {
            categories[i].getElementsByClassName("collapse-btn")[0].innerText = `${name} - ${local_calories} kkal.`
        } else {
            categories[i].getElementsByClassName("collapse-btn")[0].innerText = name
        }
    }

    document.getElementById("proteinsTotal").value = proteins.toFixed(2)
    document.getElementById("fatsTotal").value = fats.toFixed(2)
    document.getElementById("carbohydratesTotal").value = carbohydrates.toFixed(2)
    document.getElementById("caloriesTotal").value = calories.toFixed(2)

}

function removeProduct(element) {
    var container = element.parentElement.children
    var category = element.id.split('_')[0]
    element.remove()
    for (let i = 0; i < container.length; i++) {
        container[i].id = `${category}_${i}`
    }
    updateTotal()
}

function setupWater(value) {
    if (value === "") 
        value = "0"
    
    document.getElementById("waterTotal").value = parseFloat(value).toFixed(2)
}

function resetWater() {
    document.getElementById("waterInput").value = ""
    setupWater("0")
}

async function createDay() {
    document.getElementById("error").hidden = true
    document.getElementById("error").innerHTML = ""

    if (!createDayForm.reportValidity()){
        document.getElementById("error").hidden = false
        document.getElementById("error").innerHTML = "Не все обязательные поля заполнены"
        return
    }

    var total_proteins = parseFloat(document.getElementById("proteinsTotal").value)
    var total_fats = parseFloat(document.getElementById("fatsTotal").value)
    var total_carbohydrates = parseFloat(document.getElementById("carbohydratesTotal").value)
    var total_calories = parseInt(document.getElementById("caloriesTotal").value)
    var water = parseFloat(document.getElementById("waterTotal").value)

    if (total_proteins == 0 && total_fats == 0 && total_carbohydrates == 0 && total_calories == 0 && water == 0) {
        document.getElementById("error").hidden = false
        document.getElementById("error").innerHTML = "Введите данные"
        return
    }

    var info = {}

    info["date"] = document.getElementById("date").valueAsDate.toLocaleDateString()
    info["total_proteins"] = total_proteins
    info["total_fats"] = total_fats
    info["total_carbohydrates"] = total_carbohydrates
    info["total_calories"] = total_calories
    info["water"] = water

    var categories = document.getElementsByClassName("category")
    for (let i = 0; i < categories.length; i++) {
        var menu = categories[i].getElementsByClassName("collapse")[0].children
        var name = categories[i].getElementsByClassName("collapse-btn")[0].innerText.split(' - ')[0].toLowerCase()
        info[name] = {}

        for (let j = 0; j < menu.length; j++) {
            info[name][menu[j].id] = {
                "proteins": parseFloat(menu[j].getElementsByClassName("product-info")[0].value),
                "fats": parseFloat(menu[j].getElementsByClassName("product-info")[1].value),
                "carbohydrates": parseFloat(menu[j].getElementsByClassName("product-info")[2].value),
                "calories": parseInt(menu[j].getElementsByClassName("product-info")[3].value),
                "grams": parseInt(menu[j].querySelector("#copygrams").value),
                "type": menu[j].querySelector("#copyname").innerText,
                "id": menu[j].querySelector("#copyname").innerText === "Recipe" ? menu[j].getAttribute("data-id") : menu[j].querySelector("#copyinputname").value
            }
        }
    }

    var url = '/api/create_day'
    if (document.getElementById("extra_info").getAttribute("data-obj") === "1") {
        url = "/api/edit_day/" + document.getElementById("extra_info").getAttribute("data-day_id")
    }

    let response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        
        body: JSON.stringify(info)
    });

    if (response.ok) {
        data = await response.json()
        if (data['success'] == true) {
            console.log("SUCCESS")
            console.log(data['message'])
            window.location.reload();
        } else {
            console.log(data['message'])
            document.getElementById("error").hidden = false
            document.getElementById("error").innerHTML = data['message']
        }
    } 
}

async function deleteDay() {
    let response = await fetch('/api/delete_day', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        
        body: JSON.stringify({
            'id': document.getElementById("extra_info").getAttribute("data-day_id")
        })
    });

    if (response.ok) {
        data = await response.json()
        if (data['success'] == true) {
            console.log("SUCCESS")
            console.log(data['message'])
            window.location.reload();
        } else {
            console.log(data['message'])
            document.getElementById("error").hidden = false
            document.getElementById("error").innerHTML = data['message']
        }
    } 
}

function redirectToDate() {
    var value = document.getElementById("date").valueAsDate
    var today = new Date()

    let diff = value.getTime() - today.getTime()
    let days = Math.ceil(diff / (1000 * 3600 * 24));
    if (days !== 0) {
        window.location.href = "/diary/" + days
    } else {
        window.location.href = "/diary"
    }
}

