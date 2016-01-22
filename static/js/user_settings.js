/**
 * Created by Alexey Kutepov on 09.10.15.
 */

/**
 * Image preview
 * @param input
 */
function onPreview(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#impPreview').attr('src', e.target.result).width("200px").height("auto");
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$(document).ready(function () {
    $('.selectpicker').selectpicker({
        style: 'btn-default',
        size: 4
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

$(function () {
    $('#datetimepickerDateOfBirth').datetimepicker({
                format: 'DD.MM.YYYY',
                locale: 'ru'
            });
});
