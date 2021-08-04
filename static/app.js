const registerBtn = document.getElementById("register-btn")
const registerForm = document.getElementById("register-form")
const emailField = document.querySelector('input[type="email"]')
const messageContainer = document.querySelector('.message')
const inputContainer = document.querySelector('.input-fields')
const submitBtn = document.querySelector('#submit-btn')
const generatingTokenDiv = document.createElement('div')
generatingTokenDiv.className = "field"
generatingTokenDiv.style.display = "flex"
generatingTokenDiv.style.alignItems = "center"
generatingTokenDiv.style.paddingLeft = '1em'
generatingTokenDiv.innerHTML = '🤓 Generating API Token...'

function showMessage(message, type) {
	messageContainer.classList.remove('is-hidden')
	messageContainer.classList.add(type === "error" ? 'is-danger' : 'is-success')
	messageContainer.innerHTML = `
	<div class="message-header">
		<p>${type}</p>
	</div>
	<div class="message-body">${message}</div>`
	setTimeout(() => {
		messageContainer.classList.add('is-hidden')
	}, 3000)
}

registerBtn.addEventListener("click", toggleForm)

function toggleForm() { registerForm.classList.toggle('is-active') }
function toggleInputs(value) {
	if (value === false) {
		submitBtn.classList.add('is-loading')
		inputContainer.appendChild(generatingTokenDiv)
		inputContainer.removeChild(emailField)
		return
	}
	submitBtn.classList.remove('is-loading')
	inputContainer.removeChild(generatingTokenDiv)
	inputContainer.appendChild(emailField)
	emailField.value = ''
}

registerForm.addEventListener('submit', e => {
	e.preventDefault()
	toggleInputs(false)
	fetch('/api/register', {
		method: 'POST',
		body: JSON.stringify({ email: emailField.value }),
		headers: { 'Content-Type': 'application/json' }
	})
		.then(res => res.json())
		.then(data => {
			toggleInputs(true)
			toggleForm()
			showMessage(data.message, data.type)
		})
		.catch(err => console.log(err.message))
})

const navBurger = document.querySelector(".navbar-burger")
navBurger.addEventListener("click", () => {
	navBurger.classList.toggle('is-active')
	document.querySelector('#navbar-menu').classList.toggle('is-active')
})

const tabs = document.querySelectorAll('.tabs > ul li')
const code = document.querySelector('.code')
tabs.forEach(tab => {
	tab.addEventListener('click', (e) => {
		e.preventDefault()
		code.querySelectorAll('div').forEach(div => div.classList.toggle("is-hidden"))
		tabs.forEach(currentTab => {
			if (currentTab == tab) {
				currentTab.classList.add('is-active')
				return
			} currentTab.classList.remove('is-active')
		})
	})
})