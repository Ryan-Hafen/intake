$(document).ready(function () {
    $("#sou_input").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#ref_list_table tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

$(document).ready(function () {
    $("#sou_input").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#sou_list_table tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

$(document).ready(function () {
    $("#usr_input").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#usr_list_table tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});
