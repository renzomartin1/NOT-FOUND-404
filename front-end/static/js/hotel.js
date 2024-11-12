const enlaces = document.querySelectorAll("a")
enlaces.forEach(function (enlace) { // Eliminamos el subrayado y otros estilos que los enlaces puedan tener 
    enlace.style.textDecoration = "none"; // Elimina el subrayado 
    enlace.style.color = "inherit"; // Hereda el color del elemento contenedor 
    enlace.style.fontStyle = "inherit"; // Hereda el estilo de fuente 
})
