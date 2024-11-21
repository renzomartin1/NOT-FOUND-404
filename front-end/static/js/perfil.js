const contactoBotones = document.querySelectorAll('.perfil-usuario__contacto')

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