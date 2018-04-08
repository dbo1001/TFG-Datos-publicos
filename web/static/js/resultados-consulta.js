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