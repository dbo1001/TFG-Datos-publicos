/**
 * Scripts para actualizar dinámicamente los resultados de la consulta.
 */

$(function (){
    // Carga el plugin dynatable para mostrar tablas bonitas
    $("table").dynatable({
        // Desactiva los parámetros en la url
        features: {
            pushState: false
        }
    });
});
