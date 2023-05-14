function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


let allInput = document.querySelectorAll(`.check-js`)

allInput.forEach((input) => {
    input.addEventListener(`input`, (e) => {
        console.log(e.target.attributes.id_reminder.value)

        $.ajax({
            url: '/reminders',
            type: 'PUT',
            // dataType: 'json',
            // contentType: "application/json; charset=utf-8",
            data: {
                id: e.target.attributes.id_reminder.value,
                checked: Number(e.target.checked),
            },
            headers: {
                "X-CSRFTOKEN": getCookie('csrftoken')
            },
            success: function (data) {
                // console.log(data);
            }
        });
    });
})

document.querySelector(`#qwertyuiopqwerty`).addEventListener(`click`, (e)=>{
            $.ajax({
            url: `/reminder/${e.target.attributes.id_reminder.value}`,
            type: 'DELETE',
            headers: {
                "X-CSRFTOKEN": getCookie('csrftoken')
            },
            success: function (data) {
                // console.log(data);
            }
        });
            window.location.replace("/reminders");
})