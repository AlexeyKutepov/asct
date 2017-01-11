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
        $("#liTestReport").removeClass( "active" );
        $("#divProbationerReport").show();
        $("#divDepartmentReport").hide();
        $("#divExamListReport").hide();
        $("#divCompanyReport").hide();
        $("#divTestReport").hide();
        window.localStorage.setItem("tab", "probationerReport")
    });

    $("#aDepartmentReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").removeClass( "active" );
        $("#liDepartmentReport").addClass( "active" );
        $("#liExamListReport").removeClass( "active" );
        $("#liCompanyReport").removeClass( "active" );
        $("#liTestReport").removeClass( "active" );
        $("#divProbationerReport").hide();
        $("#divDepartmentReport").show();
        $("#divExamListReport").hide();
        $("#divCompanyReport").hide();
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
        $("#divTestReport").show();
        window.localStorage.setItem("tab", "testReport")
    });

    $('.selectpicker').selectpicker({
        style: 'btn-default',
        size: 4
    });
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