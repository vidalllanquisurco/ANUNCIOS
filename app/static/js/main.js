// app/static/js/main.js

document.addEventListener("DOMContentLoaded", function() {
    console.log("Tablón de Anuncios - JavaScript cargado correctamente.");
    
    // Opcional: Desaparecer alertas flash automáticamente después de 4 segundos
    setTimeout(function() {
        let alertas = document.querySelectorAll('.alert');
        alertas.forEach(function(alerta) {
            let bsAlert = new bootstrap.Alert(alerta);
            bsAlert.close();
        });
    }, 4000);
});