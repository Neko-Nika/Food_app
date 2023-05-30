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

//получаем все чекбоксы на странице
let allInput = document.querySelectorAll(`.check-js`)

allInput.forEach((input) => {
    //каждому чекбоксу вешаем лисенер на переключение
    input.addEventListener(`input`, (e) => {
        // console.log(e.target.attributes.id_reminder.value)
        //отправляем запрос на сервер для того что бы поменять значение в бд(как строится запрос, думаю понятно и в объяснении не нуждается, все есть в офф доках jquery
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
            //запрос на удаление напоминания при клике на кнопку удаления(да, id у этой кнопки интересный и суперуникальный))))
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