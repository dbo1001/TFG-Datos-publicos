/**
 * Scripts para actualizar dinámicamente la página de consulta.
 */

var fuentes, columnas, comparadores, valores;
var mostrar, descripcion, descripcionTitulo;
var listaMostrar = [];

/**
 * Actualiza las variables globales.
 * Para elementos generados dinámicamente.
 */
function actualizaVariables() {
    fuentes = $("#consulta [name^=fuente-]");
    columnas = $("#consulta [name^=columna_filtro-]");
    comparadores = $("#consulta [name^=comparador-]");
    valores = $("#consulta [name^=valor-]");
}

/**
 * Obtiene el id de un selector a partir de su nombre
 */
function getId(element) {
    var name = element.getAttribute("name");
    return name.split("-").pop();
}

/**
 * Muestra la subconsulta correspondiente al selector
 */
function muestraSubconsulta(selector) {
    var parent = $(selector).parent("li");
    var activa = parent.hasClass("active");
    var subconsultas = $("#consulta .subconsulta");
    var tabs = $("#subconsulta-tab li");
    if (!activa) {
        var id = tabs.index(parent);
        subconsultas.hide();
        var subconsulta = $(subconsultas.get(id));
        subconsulta.show();
    }
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
 * Actualiza la lista de columnas a mostrar
 */
function actualizaColumnasMostrar() {
    var opciones = [];
    mostrar.empty();
    listaMostrar = [];

    columnas.each(function(i, selFiltro){
        var filtro = $(selFiltro);
        var opcionesColumna = filtro.find("option");
        opcionesColumna.each(function(j, selColumna) {
            var columna = $(selColumna);
            var valor = columna.val();
            opciones.push(valor);
        });
    });

    // Elimina duplicados y columna artificial "Todas"
    opciones = new Set(opciones);
    opciones.delete("Todas");

    // Añade las opciones a la lista
    opciones.forEach(function(valor) {
        listaMostrar.push(valor);
        mostrar.append(new Option(valor));
    });
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
 * Añade una subconsulta
 */
function addSubconsulta(id) {
    var subconsultas = $("#consulta .subconsulta");
    var template = $("#subconsulta-template .subconsulta");
    var ultima = subconsultas.last();
    // Clona el template
    var nueva = template.clone();
    var html = $(nueva).prop("outerHTML");
    // Cambia los id de todos los atributos por el correspondiente
    var regex = new RegExp("-0", "g");
    html = html.replace(regex, "-" + (id - 1));
    $(ultima).after(html);
    $("#join").show();
}

/**
 * Actualiza los eventos
 */
function actualizaEventos() {
    // Elimina eventos existentes
    fuentes.unbind();
    columnas.unbind();

    // Actualiza cada vez que cambie el valor de fuente
    fuentes.on("change", function () {
        var id = getId(this);
        actualizaColumnas(id);
    });

    columnas.on("change", function () {
        var id = getId(this);
        actualizaComparador(id);
    });
}

/**
 * Autocompleta la columna calculada con el valor de las columnas.
 * Basado en: http://jqueryui.com/autocomplete/#categories
 */
function autocompletarColumnaCalculada() {
    // Separa las columnas calculadas
    function split(val) {
        return val.split(/ \s*/);
    }

    // Extrae la seleccionada
    function extractLast(term) {
        return split(term).pop();
    }

    $("#columna_calculada")
        // don't navigate away from the field on tab when selecting an item
        .on("keydown", function(event) {
            if (event.keyCode === $.ui.keyCode.TAB &&
                $(this).autocomplete("instance").menu.active) {
                event.preventDefault();
            }
        })
        .autocomplete({
            minLength: 0,
            source(request, response) {
                // delegate back to autocomplete, but extract the last term
                response($.ui.autocomplete.filter(
                    listaMostrar, extractLast(request.term)));
            },
            focus() {
                // prevent value inserted on focus
                return false;
            },
            select(event, ui) {
                var terms = split(this.value);
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push(ui.item.value);
                // add placeholder to get the comma-and-space at the end
                terms.push("");
                this.value = terms.join(" ");
                return false;
            }
        });
}


// Al cargar la página
$(function() {

    mostrar = $("#select_mostrar");
    descripcion = $("#descripcion");
    descripcionTitulo = $("#descripcion_titulo");

    actualizaVariables();
    actualizaEventos();
    autocompletarColumnaCalculada();

    // Llama primero al cargar la página
    columnas.each(function(id){
        actualizaColumnas(id);
    });

    // Pestañas de la consulta
    $("#subconsulta-tab").on("click", "li a", function () {
        muestraSubconsulta(this);
    });

    // Evento para añadir una subconsulta
    $("#add-subconsulta").click(function (e) {
        e.stopPropagation();
        var tabs = $("#subconsulta-tab li");
        var id = tabs.children().length;
        var item = $("<li><a href=\"#\" data-toggle=\"tab\">Consulta " + id + "</a></li>");
        addSubconsulta(id);
        actualizaVariables();
        actualizaEventos();
        $(this).closest("li").before(item);
        $("#subconsulta-tab li:nth-child(" + id + ") a").click();
    });

    // Activa todos los campos al enviar el formulario
    $("form").submit(function() {
        $("#subconsulta-template").remove();
        $("input, select").attr("disabled", false);
    });
});
