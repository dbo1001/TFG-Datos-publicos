/**
 * Scripts para actualizar dinámicamente la página de consulta.
 */

$(function() {

    /**
     * Actualiza los campos del formulario según la fuente seleccionada.
     */
    var fuentes = $("[name^=fuente-]");
    var columnas = $("[name^=columna_filtro-]");
    var mostrar = $("#select_mostrar");
    var comparadores = $("[name^=comparador-]");
    var valores = $("[name^=valor-]");
    var descripcion = $("#descripcion");
    var descripcionTitulo = $("#descripcion_titulo");

    /**
     * Obtiene el id de un selector a partir de su nombre
     */
    function getId(element) {
        var name = element.getAttribute("name");
        return name.split("-").pop();
    }

    /**
     * Activa o desactiva el comparador según el parámetro
     */
    function actualizaComparador(id) {
        var columna = $(columnas.get(id));
        var valor = $(valores.get(id));
        var comparador = $(comparadores.get(id));
        if (columna.val() === "Todas") {
            // Desactiva el comparador
            comparador.attr("disabled", true);
            valor.attr("disabled", true);
        } else {
            // Activa el comparador
            comparador.removeAttr("disabled");
            valor.removeAttr("disabled");
        }
    }

    /**
     * Consulta información sobre una fuente de datos al servidor
     */
    function datosFuente(nombreFuente, callback) {
        $.ajax({
            type: "GET",
            url: "/api/fuente/" + nombreFuente
        }).done(callback);
    }

    /**
     * Actualiza las columnas al seleccionar una fuente
     */
    function actualizaColumnas(id) {
        var columna = $(columnas.get(id));
        var fuente = fuentes.get(id).value;
        
        // Limpia las columnas
        columna.attr("disabled", true);
        columna.empty();

        datosFuente(fuente, function(data) {
            var columnasFuente = data["columnas"];
            var descripcionFuente = data["descripcion"];

            columnasFuente.forEach(function(item) {
                // Añade todas las columnas
                columna.append(new Option(item));
            });

            columna.removeAttr("disabled");
            descripcion.text(descripcionFuente);
            descripcionTitulo.text(fuente);
            actualizaComparador(id);
            actualizaColumnasMostrar();
        });
    }

    /**
     * Actualiza la lista de columnas a mostrar
     */
    function actualizaColumnasMostrar() {
        var opciones = [];
        mostrar.empty();

        columnas.each(function(i, sel_filtro){
            var filtro = $(sel_filtro);
            var opciones_columna = filtro.find("option");
            opciones_columna.each(function(j, sel_columna) {
                var columna = $(sel_columna);
                var valor = columna.val();
                opciones.push(valor);
            });
        });

        // Elimina duplicados y columna artificial "Todas"
        opciones = new Set(opciones);
        opciones.delete("Todas");

        // Añade las opciones a la lista
        opciones.forEach(function(valor) {
            mostrar.append(new Option(valor));
        });
    }

    // Llama primero al cargar la página
    columnas.each(function(id){
        actualizaColumnas(id);
    });

    // Actualiza cada vez que cambie el valor de fuente
    fuentes.on("change", function() {
        var id = getId(this);
        actualizaColumnas(id);
    });

    columnas.on("change", function() {
        var id = getId(this);
        console.log(this);
        console.log(id);
        actualizaComparador(id);
    });

});
