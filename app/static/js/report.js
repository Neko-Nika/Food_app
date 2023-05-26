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

function redirectToDate() {
    var value = document.getElementById("date").valueAsDate
    var today = new Date()

    let diff = value.getTime() - today.getTime()
    let days = Math.ceil(diff / (1000 * 3600 * 24));
    if (days !== 0) {
        window.location.href = "/report/" + days
    } else {
        window.location.href = "/report"
    }
}
