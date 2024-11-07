// La etiqueta dialog ya tiene en el dom incorporado algunos métodos en js, como el de abrirlo
// <dialogtraidoajspordom>.showModal()

// La etiqueta dialog ya viene incorporado algunos métodos en js, como el de cerrarlo
// <dialogtraidoajspordom>.close()

const botonAbrirModalLogin = document.getElementById("boton-abrir-modal-login")
const botonCerrarModalLogin = document.getElementById("boton-cerrar-modal-login")
const modalLogin = document.getElementById("contenedor-modal-login")

botonAbrirModalLogin.addEventListener("click", () => {
    modalLogin.showModal()
})

botonCerrarModalLogin.addEventListener("click", () => {
    modalLogin.close()
})




const botonAbrirModalRegister = document.getElementById("boton-abrir-modal-register")
const botonCerrarModalRegister = document.getElementById("boton-cerrar-modal-register")
const modalRegister = document.getElementById("contenedor-modal-register")

botonAbrirModalRegister.addEventListener("click", () => {
    modalRegister.showModal()
})

botonCerrarModalRegister.addEventListener("click", () => {
    modalRegister.close()
})