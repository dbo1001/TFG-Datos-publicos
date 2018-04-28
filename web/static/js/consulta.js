/**
 * Scripts para actualizar dinámicamente la página de consulta.
 */

var fuentes, columnas, comparadores, valores;
var mostrar, descripcion, descripcionTitulo;


/**
 * Actualiza las variables globales.
 * Para elementos generados dinámicamente.
 */
function actualizaVariables() {
    fuentes = $("[name^=fuente-]");
    columnas = $("[name^=columna_filtro-]");
    comparadores = $("[name^=comparador-]");
    valores = $("[name^=valor-]");
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
    var subconsultas = $(".subconsulta");
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
function addSubconsulta() {
    var subconsultas = $(".subconsulta");
    var ultima = subconsultas.last();
    var idUltima = subconsultas.index(ultima);
    var id = idUltima + 1;
    var nueva = ultima.clone();
    var html = $(nueva).prop("outerHTML");
    var regex = new RegExp("-" + idUltima, "g");
    html = html.replace(regex, "-" + id);
    $(ultima).after(html);
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



// Al cargar la página
$(function() {

    mostrar = $("#select_mostrar");
    descripcion = $("#descripcion");
    descripcionTitulo = $("#descripcion_titulo");

    actualizaVariables();
    actualizaEventos();

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
        addSubconsulta();
        actualizaVariables();
        actualizaEventos();
        $(this).closest("li").before(item);
        $("#subconsulta-tab li:nth-child(" + id + ") a").click();
    });
});
