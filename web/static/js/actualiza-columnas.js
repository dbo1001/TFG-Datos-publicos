$(function() {

    var fuente = $('#select_fuente');
    var columna = $('#select_columna');

    // Llama primero al cargar la página
    actualizaColumnas();

    // Actualiza las columnas al seleccionar una fuente
    function actualizaColumnas() {
        var send = {
            fuente: fuente.val()
        };

        columna.attr('disabled', 'disabled');
        columna.empty();

        // Envía la fuente y recibe las columnas de esta fuente
        $.getJSON("/api/actualiza_columnas/" + fuente.val(), function(data) {
            data.forEach(function(item) {
                columna.append(
                    $('<option>', {
                        value: item,
                        text: item
                        // value: item[0],
                        // text: item[1]
                    })
                );
            });
            columna.removeAttr('disabled');
        });
    }

    // Actualiza cada vez que cambie el valor de fuente
    fuente.on('change', function() {
        actualizaColumnas();
    });

});