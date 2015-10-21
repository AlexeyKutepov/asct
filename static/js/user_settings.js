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

    //$.ajax({
    //    type: "POST",
    //    url: "/get/department/list/",
    //    data: {
    //        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
    //        id: $("#selectCompany").val()
    //    },
    //    success: function(data) {
    //        $("#selectDepartment > option").each(function() {
    //            $(this).remove();
    //        });
    //        var departmentList = data["department_list"];
    //        var result = "";
    //        for (var i = 0; i < departmentList.length; i++) {
    //            result += "<option value=\"" + departmentList[i]["id"] + "\">" + departmentList[i]["name"] + "</option>";
    //        }
    //        $("#selectDepartment").append(result);
    //    },
    //    error: function(xhr, textStatus, errorThrown) {
    //        alert("Error: "+errorThrown+xhr.status+xhr.responseText);
    //    }
    //});
});
