$(document).ready(function () {

    var addDepartment = function() {
        var isAdd = true;

        $("#tableDepartmentList > tbody > tr").each(function () {
            if ($(this).find("td:first").html() == $("#inputDepartment").val()) {
                alert("Подразделение " + $("#inputDepartment").val() + " уже существует!")
                isAdd = false;
            }
        });

        if (isAdd) {
            $("#tableDepartmentList").append(
                    "<tr><td>" + $("#inputDepartment").val() + "</td><td ><input type=\"hidden\" name=\"department\" value=\"" + $("#inputDepartment").val() + "\" /></td><td><button name=\"buttonDelete\" type=\"button\" class=\"btn btn-danger pull-right\" title=\"Удалить подразделение\"><span class=\"glyphicon glyphicon-trash\" aria-hidden=\"true\"></span></button></td></tr>"
            );
        }
        $("#inputDepartment").val("");
    };

    $("#buttonDepartmentAdd").click(addDepartment);

    $('#tableDepartmentList').on( "click", "button[name='buttonDelete']", function() {
        var rowIndex = $(this).parent().parent().remove();
        return false;
    });
});
