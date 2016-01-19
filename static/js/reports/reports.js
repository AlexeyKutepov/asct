/**
 * Created by alexey on 25.12.15.
 */

$(document).ready(function () {

    if (supports_html5_storage) {
        var tab = window.localStorage.getItem("tab");
        if (tab == "departmentReport") {
            $("#liProbationerReport").removeClass( "active" );
            $("#liDepartmentReport").addClass( "active" );
            $("#liExamListReport").removeClass( "active" );
            $("#liCompanyReport").removeClass( "active" );
            $("#liAllCompanyReport").removeClass( "active" );
            $("#liTestReport").removeClass( "active" );
            $("#divProbationerReport").hide();
            $("#divDepartmentReport").show();
            $("#divExamListReport").hide();
            $("#divCompanyReport").hide();
            $("#divAllCompanyReport").hide();
            $("#divTestReport").hide();
        } else if (tab == "examListReport") {
            $("#liProbationerReport").removeClass( "active" );
            $("#liDepartmentReport").removeClass( "active" );
            $("#liExamListReport").addClass( "active" );
            $("#liCompanyReport").removeClass( "active" );
            $("#liAllCompanyReport").removeClass( "active" );
            $("#liTestReport").removeClass( "active" );
            $("#divProbationerReport").hide();
            $("#divDepartmentReport").hide();
            $("#divExamListReport").show();
            $("#divCompanyReport").hide();
            $("#divAllCompanyReport").hide();
            $("#divTestReport").hide();
        } else if (tab == "companyReport") {
            $("#liProbationerReport").removeClass( "active" );
            $("#liDepartmentReport").removeClass( "active" );
            $("#liExamListReport").removeClass( "active" );
            $("#liCompanyReport").addClass( "active" );
            $("#liAllCompanyReport").removeClass( "active" );
            $("#liTestReport").removeClass( "active" );
            $("#divProbationerReport").hide();
            $("#divDepartmentReport").hide();
            $("#divExamListReport").hide();
            $("#divCompanyReport").show();
            $("#divAllCompanyReport").hide();
            $("#divTestReport").hide();
        } else if (tab == "allCompanyReport") {
            $("#liProbationerReport").removeClass( "active" );
            $("#liDepartmentReport").removeClass( "active" );
            $("#liExamListReport").removeClass( "active" );
            $("#liCompanyReport").removeClass( "active" );
            $("#liAllCompanyReport").addClass( "active" );
            $("#liTestReport").removeClass( "active" );
            $("#divProbationerReport").hide();
            $("#divDepartmentReport").hide();
            $("#divExamListReport").hide();
            $("#divCompanyReport").hide();
            $("#divAllCompanyReport").show();
            $("#divTestReport").hide();
        } else if (tab == "testReport") {
            $("#liProbationerReport").removeClass( "active" );
            $("#liDepartmentReport").removeClass( "active" );
            $("#liExamListReport").removeClass( "active" );
            $("#liCompanyReport").removeClass( "active" );
            $("#liAllCompanyReport").removeClass( "active" );
            $("#liTestReport").addClass( "active" );
            $("#divProbationerReport").hide();
            $("#divDepartmentReport").hide();
            $("#divExamListReport").hide();
            $("#divCompanyReport").hide();
            $("#divAllCompanyReport").hide();
            $("#divTestReport").show();
        }
    }

    $("#aProbationerReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").addClass( "active" );
        $("#liDepartmentReport").removeClass( "active" );
        $("#liExamListReport").removeClass( "active" );
        $("#liCompanyReport").removeClass( "active" );
        $("#liAllCompanyReport").removeClass( "active" );
        $("#liTestReport").removeClass( "active" );
        $("#divProbationerReport").show();
        $("#divDepartmentReport").hide();
        $("#divExamListReport").hide();
        $("#divCompanyReport").hide();
        $("#divAllCompanyReport").hide();
        $("#divTestReport").hide();
        window.localStorage.setItem("tab", "probationerReport")
    });

    $("#aDepartmentReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").removeClass( "active" );
        $("#liDepartmentReport").addClass( "active" );
        $("#liExamListReport").removeClass( "active" );
        $("#liCompanyReport").removeClass( "active" );
        $("#liAllCompanyReport").removeClass( "active" );
        $("#liTestReport").removeClass( "active" );
        $("#divProbationerReport").hide();
        $("#divDepartmentReport").show();
        $("#divExamListReport").hide();
        $("#divCompanyReport").hide();
        $("#divAllCompanyReport").hide();
        $("#divTestReport").hide();
        window.localStorage.setItem("tab", "departmentReport")
    });

    $("#aExamListReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").removeClass( "active" );
        $("#liDepartmentReport").removeClass( "active" );
        $("#liExamListReport").addClass( "active" );
        $("#liCompanyReport").removeClass( "active" );
        $("#liAllCompanyReport").removeClass( "active" );
        $("#liTestReport").removeClass( "active" );
        $("#divProbationerReport").hide();
        $("#divDepartmentReport").hide();
        $("#divExamListReport").show();
        $("#divCompanyReport").hide();
        $("#divAllCompanyReport").hide();
        $("#divTestReport").hide();
        window.localStorage.setItem("tab", "examListReport")
    });

    $("#aCompanyReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").removeClass( "active" );
        $("#liDepartmentReport").removeClass( "active" );
        $("#liExamListReport").removeClass( "active" );
        $("#liCompanyReport").addClass( "active" );
        $("#liAllCompanyReport").removeClass( "active" );
        $("#liTestReport").removeClass( "active" );
        $("#divProbationerReport").hide();
        $("#divDepartmentReport").hide();
        $("#divExamListReport").hide();
        $("#divCompanyReport").show();
        $("#divAllCompanyReport").hide();
        $("#divTestReport").hide();
        window.localStorage.setItem("tab", "companyReport")
    });

    $("#aAllCompanyReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").removeClass( "active" );
        $("#liDepartmentReport").removeClass( "active" );
        $("#liExamListReport").removeClass( "active" );
        $("#liCompanyReport").removeClass( "active" );
        $("#liAllCompanyReport").addClass( "active" );
        $("#liTestReport").removeClass( "active" );
        $("#divProbationerReport").hide();
        $("#divDepartmentReport").hide();
        $("#divExamListReport").hide();
        $("#divCompanyReport").hide();
        $("#divAllCompanyReport").show();
        $("#divTestReport").hide();
        window.localStorage.setItem("tab", "allCompanyReport")
    });

    $("#aTestReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").removeClass( "active" );
        $("#liDepartmentReport").removeClass( "active" );
        $("#liExamListReport").removeClass( "active" );
        $("#liCompanyReport").removeClass( "active" );
        $("#liAllCompanyReport").removeClass( "active" );
        $("#liTestReport").addClass( "active" );
        $("#divProbationerReport").hide();
        $("#divDepartmentReport").hide();
        $("#divExamListReport").hide();
        $("#divCompanyReport").hide();
        $("#divAllCompanyReport").hide();
        $("#divTestReport").show();
        window.localStorage.setItem("tab", "testReport")
    });

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

    $("#selectCompany").trigger( "change" );

});


/**
 * Проверяем доступность локального хранилища
 * @returns {boolean}
 */
function supports_html5_storage() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
} catch (e) {
    return false;
  }
}