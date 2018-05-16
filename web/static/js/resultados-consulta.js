/**
 * Scripts para actualizar dinámicamente los resultados de la consulta.
 */

/**
 * Cambia el método en el enlace para mostrar el mapa.
 */
function cambiaEnlace(selector, metodo, posicion) {
    selector = $(selector);
    var href = selector.attr("href");
    var ruta = href.split("/");
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
            cambiaEnlace(this, valor, 4);
        });
    });

    // Cada vez que cambia el territorio para visualizar el mapa
    territorio.change(function () {
        var valor = this.value;
        visualizaMapa.each(function() {
            cambiaEnlace(this, valor, 3);
        });
    });


});
