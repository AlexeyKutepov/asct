$(document).ready(function () {

    var curatorSearch = function() {

        $("#tableDepartmentList").append(
            "<tr><td>" + $("#inputDepartment").val() + "</td><td><button name=\"buttonDelete\" type=\"button\" class=\"btn btn-danger pull-right\" title=\"Удалить подразделение\"><span class=\"glyphicon glyphicon-trash\" aria-hidden=\"true\"></span></button></td></tr>"
        );
        $("#inputDepartment").val("");
    };

    $("#buttonDepartmentAdd").click(curatorSearch);

    $('#tableDepartmentList').on( "click", "button[name='buttonDelete']", function() {
        var rowIndex = $(this).parent().parent().remove();
        return false;
    });
});
