const botonAbrirModalLogin = document.getElementById("boton-abrir-modal-login")
const botonCerrarModalLogin = document.getElementById("boton-cerrar-modal-login")
const modalLogin = document.getElementById("contenedor-modal-login")

botonAbrirModalLogin.addEventListener("click", () => {
    modalLogin.showModal()
})

botonCerrarModalLogin.addEventListener("click", () => {
    modalLogin.close()
})

// botonAbrirModalLogin: El botón que aparece en la derecha superior de la página web y cuyo texto es "Iniciar sesión".
// botonCerrarModalLogin: El botón con "X" que aparece una vez que se abre el modal login.
// modalLogin: La ventana modal (o emergente) que contiene el formulario de ingreso.

// 1er Evento: Una vez que botonAbrirModalLogin es apretado, el modal login aparece.
// 2do Evento: Una vez que botonCerrarModalLogin es apretado, el modal login desaparece.




const botonAbrirModalRegister = document.getElementById("boton-abrir-modal-register")
const botonCerrarModalRegister = document.getElementById("boton-cerrar-modal-register")
const modalRegister = document.getElementById("contenedor-modal-register")

botonAbrirModalRegister.addEventListener("click", () => {
    modalRegister.showModal()
})

botonCerrarModalRegister.addEventListener("click", () => {
    modalRegister.close()
})

// botonAbrirModalRegister: El botón que aparece en la derecha superior de la página web y cuyo texto es "Registrarse".
// botonCerrarModalRegister: El botón con "X" que aparece una vez que se abre el modal register.
// modalRegister: La ventana modal (o emergente) que contiene el formulario de registro.

// 1er Evento: Una vez que botonAbrirModalRegister es apretado, el modal register aparece.
// 2do Evento: Una vez que botonCerrarModalRegister es apretado, el modal register desaparece.




const textoRegisterModalLogin = document.getElementById("texto-register-modal-login")
const textoLoginModalRegister = document.getElementById("texto-login-modal-register")

textoRegisterModalLogin.addEventListener("click", () => {
    modalLogin.close()
    modalRegister.showModal()
})

textoLoginModalRegister.addEventListener("click", () => {
    modalRegister.close()
    modalLogin.showModal()
})

// textoRegisterModalLogin: El texto "Registrarse" que aparece una vez que se abre el modal login.
// textoLoginModalRegister: El texto "Inicia sesión" que aparece una vez que se abre el modal register.

// 1er Evento: Una vez que textoRegisterModalLogin es apretado, el modal login desaparece y el modal register aparece.
// 2do Evento: Una vez que textoLoginModalRegister es apretado, el modal register desaparece y el modal login aparece.