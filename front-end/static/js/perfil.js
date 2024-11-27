const contactoBotones = document.querySelectorAll('.perfil-usuario__contacto');

function copiarContactoContenido(contactoBtn) {
  const notifActivas = contactoBtn.parentElement.querySelectorAll('.texto-copiado-notif');
  notifActivas.forEach(notifActiva => { notifActiva.remove(); });
  
  const notif = document.createElement('div');
  notif.textContent = '¡Texto copiado!';
  notif.classList.add('texto-copiado-notif');
  notif.addEventListener('click', () => { notif.remove(); });
  contactoBtn.parentElement.append(notif);

  let span = contactoBtn.querySelector('span');
  navigator.clipboard.writeText(span.textContent);
}

for (const contactoBtn of contactoBotones) {
  contactoBtn.addEventListener('click', () => { copiarContactoContenido(contactoBtn); });
}

const eliminarCuentaBoton = document.querySelector('.eliminar-cuenta-boton');
const confirmarEliminacionModal = document.getElementById('contenedor-confirmar-eliminacion-modal');
const cancelarBoton = document.getElementById('cancelar-eliminacion-boton');

eliminarCuentaBoton.addEventListener('click', () => {
  confirmarEliminacionModal.showModal();
});

cancelarBoton.addEventListener('click', () => {
  confirmarEliminacionModal.close();
});

const eliminarReservaBotones = document.querySelectorAll('.eliminar-reserva-boton');

eliminarReservaBotones.forEach(boton => {
    boton.addEventListener('click', () => {
        // Obtiene el siguiente elemento al boton para "abrirlo"(el dialog correspondiente)
        const modal = boton.nextElementSibling;
        if (modal.tagName === 'DIALOG') {
            modal.showModal();
        }
    });
});

const cancelarBotones = document.querySelectorAll('.cancelar-eliminacion-boton-reserva');

cancelarBotones.forEach(boton => {
    boton.addEventListener('click', () => {
        // Encuentra el dialog mas cercano al boton para cerrarlo (hacia arriba)
        const modal = boton.closest('dialog');
        if (modal) {
            modal.close();
        }
    });
});
