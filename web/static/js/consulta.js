/**
 * Scripts para actualizar dinámicamente la página de consulta.
 */

$(function() {

    /**
     * Actualiza los campos del formulario según la fuente seleccionada.
     */
    var fuente = $("#select_fuente");
    var columna = $("#select_columna");
    var comparador = $("#select_comparador");
    var valor = $("#select_valor");

    function activaComparador() {
        comparador.removeAttr("disabled");
        valor.removeAttr("disabled");
    }

    function desactivaComparador() {
        comparador.attr("disabled", true);
        valor.attr("disabled", true);
    }

    // Actualiza las columnas al seleccionar una fuente
    function actualizaColumnas() {
        columna.attr("disabled", true);
        columna.empty();

        // Envía la fuente y recibe las columnas de esta fuente
        $.getJSON("/api/actualiza_columnas/" + fuente.val(), function(data) {
            data.forEach(function(item) {
                columna.append(
                    $("<option>", {
                        value: item,
                        text: item
                    })
                );
            });
            columna.removeAttr("disabled");
        });
    }

    // Llama primero al cargar la página
    actualizaColumnas();

    // Actualiza cada vez que cambie el valor de fuente
    fuente.on("change", function() {
        actualizaColumnas();
    });

    columna.on("change", function() {
        if (columna.val() == "Todas") {
            desactivaComparador();
        } else {
            activaComparador();
        }
    });

});