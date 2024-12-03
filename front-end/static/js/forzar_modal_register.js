modalRegister.showModal()
/*
Este script fuerza la apertura del modal register y solo se ejecutará cuando se renderice home.html luego de que:

- Desde el modal register se intenta registrar un usuario cuyas contraseñas no coinciden (mensaje de error).
- Desde el modal register se intenta registrar un correo electrónico o un número telefónico ya registrado (mensaje de error).
- Desde el modal register se intentan registrar un correo electrónico y un número telefónico ya registrados (mensaje de error).
*/