/**
 * Scripts para actualizar dinámicamente los resultados de la consulta.
 */

function descargaConsulta(formato) {
    /**
     * Descarga una consulta en un formato.
     */
    // Guarda el formato en una cookie
    document.cookie="descarga=" + formato;
    // Recarga la página
    window.location.reload(true);
}

$(function (){
    // Carga el plugin dynatable para mostrar tablas bonitas
    $("table").dynatable({
        // Desactiva los parámetros en la url
        features: {
            pushState: false
        }
    });
});
