/**
 * Scripts para actualizar dinámicamente los resultados de la consulta.
 */

/**
 * Cambia el método en el enlace para mostrar el mapa.
 */
function cambiaEnlace(selector, metodo) {
    selector = $(selector);
    var href = selector.attr("href");
    var ruta = href.split("/");
    var posicion = metodo.length > 5 ? 3 : 4;
    ruta[posicion] = metodo;
    href = ruta.join("/");
    selector.attr("href", href);
}


$(function (){
    // Carga el plugin dynatable para mostrar tablas bonitas
    $("table").dynatable({
        // Desactiva los parámetros en la url
        features: {
            pushState: false
        }
    });

    var metodoMapa = $("#metodo-mapa");
    var territorio = $("#territorio");
    var visualizaMapa = $("#visualiza-mapa a");

    // Cada vez que cambia el método para visualizar el mapa
    metodoMapa.change(function () {
        var valor = this.value;
        visualizaMapa.each(function() {
            cambiaEnlace(this, valor);
        });
    });

    // Cada vez que cambia el territorio para visualizar el mapa
    territorio.change(function () {
        var valor = this.value;
        visualizaMapa.each(function() {
            cambiaEnlace(this, valor);
        });
    });


});
