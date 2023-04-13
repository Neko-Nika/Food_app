window.onload = () => {
    signUpBtn.onclick = createAccount
}

async function createAccount(event) {
    if (!create_account.reportValidity()){
        console.log("Error in form")
        return
      }

    let response = await fetch('/api/create_account', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        
        body: JSON.stringify({
            'username': usernameInput.value, 'firstname': firstnameInput.value, 'lastname': lastnameInput.value,
            'email': emailInput.value, 'password': passwordInput.value, 'repeatpassword': repeatpasswordInput.value
        })
    });

    if (response.ok) {
        data = await response.json()
        if (data['success'] == true) {
            window.location.replace("/");
        } else {
            console.log(data['message'])
            document.getElementById("error").hidden = false
            document.getElementById("error").innerHTML = data['message']
        }
    } 
}
