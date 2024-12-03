document.querySelectorAll(".viewmore-button").forEach(boton => {
    boton.addEventListener("click", (event) => {
        const url = event.target.getAttribute("data-url");
        window.location.href = url;
    });
});