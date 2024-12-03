modalLogin.showModal()
/*
Este script fuerza la apertura del modal login y solo se ejecutará cuando se renderice home.html luego de que:

- Desde el modal register se registra un usuario correctamente (mensaje de éxito).
- Desde el modal login se intenta ingresar con un correo electrónico no registrado (mensaje de error).
- Desde el modal login se intenta ingresar con un correo electrónico registrado, pero con una contraseña incorrecta (mensaje de error).
*/