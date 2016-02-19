/**
 * Created by alexey on 19.02.16.
 */
$(document).ready(function () {
    $('.selectpicker').selectpicker({
        style: 'btn-default',
        size: 4
    });

    $("#checkboxBindDepartment").click(function() {
        $("#selectDepartment").attr('disabled', !this.checked).selectpicker('refresh');
    });

    $("#selectCompany").change(function() {
        $.ajax({
            type: "POST",
            url: "/get/department/list/",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                id: $(this).val()
            },
            success: function (data) {
                $('#selectDepartment')
                    .find('option')
                    .remove()
                    .end()
                    .selectpicker('refresh')
                ;
                var departmentList = data["department_list"];
                for (var i = 0; i < departmentList.length; i++) {
                    $('#selectDepartment').append($("<option/>", {
                        value: departmentList[i]["id"],
                        text: departmentList[i]["name"]
                    })).selectpicker('refresh');
                }
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log("Error: " + errorThrown + xhr.status + xhr.responseText);
            }
        });
    });
});