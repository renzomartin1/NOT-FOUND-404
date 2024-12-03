
/*
// Variables globales
const subtotal = 200; // Ejemplo de precio del hotel
const taxRate = 0.13; // 13% de impuesto

// Calcula el total y actualiza el ticket de compra
function updateTicket() {
    const tax = subtotal * taxRate;
    const total = subtotal + tax;

    // Actualizar los elementos del ticket
    document.getElementById('subtotal').textContent = `₡${subtotal.toFixed(2)}`;
    document.getElementById('tax').textContent = `₡${tax.toFixed(2)}`;
    document.getElementById('total').textContent = `₡${total.toFixed(2)}`;
}

// Manejar el envío del formulario de información del comprador
document.getElementById('buyer-info-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita que el formulario se envíe de manera predeterminada

    // Obtener la información del comprador
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;

    // Mostrar un mensaje de bienvenida 
    alert(`Gracias por tu reserva, ${firstName} ${lastName}. El total es de ₡${(subtotal + subtotal * taxRate).toFixed(2)}.`);

    // Actualizar el ticket de compra
    updateTicket();
});*/

// Validar la información de la tarjeta de crédito antes de realizar el pago
/*document.getElementById('payment-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita que el formulario se envíe de manera predeterminada

    const cardNumber = document.getElementById('card-number').value;
    const expiryDate = document.getElementById('expiry-date').value;
    const cvv = document.getElementById('cvv').value;
    const cardholderName = document.getElementById('cardholder-name').value;

    // Validaciones simples
    if (!cardNumber || !expiryDate || !cvv || !cardholderName) {
        alert("Por favor, complete toda la información de pago.");
        return;
    }

    // Aquí podrías hacer una solicitud a una API de pago (esto es solo un ejemplo)
    alert('Pago procesado con éxito. ¡Gracias por tu compra!');
});*/
