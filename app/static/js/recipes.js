function filterRecipes(element) {
    const text = element.value.toUpperCase()
    const cards = document.getElementsByClassName("col")
    
    for (let i = 0; i < cards.length; i++) {
        let title = cards[i].querySelector(".card .card-body .card-title");
        let cardUser = cards[i].querySelector(".card .card-footer .card-text")
        let check = document.getElementById("OnlyMyRecipesCheck")
        let user = null
        if (check) {
            user = check.getAttribute("data-user")
        }

        if (title.innerText.toUpperCase().indexOf(text) > -1) {
            if (user && check.checked === true) {
                if (cardUser.innerText === '@' + user) {
                    cards[i].hidden = false
                } else {
                    cards[i].hidden = true
                }
            } else {
                cards[i].hidden = false
            }
        } else {
            cards[i].hidden = true
        }
    }
}

function showMyRecipes(element) {
    document.getElementById("inputSearch").value = ""
    filterRecipes(document.getElementById("inputSearch"))
}

function goToRecipe(element) {
    const id = element.getAttribute("data-id")
    window.location.replace("recipe/" + id)
}
