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
            $("#divProbationerReport").hide();
            $("#divDepartmentReport").show();
            $("#divExamListReport").hide();
            $("#divCompanyReport").hide();
            $("#divAllCompanyReport").hide();
        } else if (tab == "examListReport") {
            $("#liProbationerReport").removeClass( "active" );
            $("#liDepartmentReport").removeClass( "active" );
            $("#liExamListReport").addClass( "active" );
            $("#liCompanyReport").removeClass( "active" );
            $("#liAllCompanyReport").removeClass( "active" );
            $("#divProbationerReport").hide();
            $("#divDepartmentReport").hide();
            $("#divExamListReport").show();
            $("#divCompanyReport").hide();
            $("#divAllCompanyReport").hide();
        } else if (tab == "companyReport") {
            $("#liProbationerReport").removeClass( "active" );
            $("#liDepartmentReport").removeClass( "active" );
            $("#liExamListReport").removeClass( "active" );
            $("#liCompanyReport").addClass( "active" );
            $("#liAllCompanyReport").removeClass( "active" );
            $("#divProbationerReport").hide();
            $("#divDepartmentReport").hide();
            $("#divExamListReport").hide();
            $("#divCompanyReport").show();
            $("#divAllCompanyReport").hide();
        } else if (tab == "allCompanyReport") {
            $("#liProbationerReport").removeClass( "active" );
            $("#liDepartmentReport").removeClass( "active" );
            $("#liExamListReport").removeClass( "active" );
            $("#liCompanyReport").removeClass( "active" );
            $("#liAllCompanyReport").addClass( "active" );
            $("#divProbationerReport").hide();
            $("#divDepartmentReport").hide();
            $("#divExamListReport").hide();
            $("#divCompanyReport").hide();
            $("#divAllCompanyReport").show();
        }
    }

    $("#aProbationerReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").addClass( "active" );
        $("#liDepartmentReport").removeClass( "active" );
        $("#liExamListReport").removeClass( "active" );
        $("#liCompanyReport").removeClass( "active" );
        $("#liAllCompanyReport").removeClass( "active" );
        $("#divProbationerReport").show();
        $("#divDepartmentReport").hide();
        $("#divExamListReport").hide();
        $("#divCompanyReport").hide();
        $("#divAllCompanyReport").hide();
        window.localStorage.setItem("tab", "probationerReport")
    });

    $("#aDepartmentReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").removeClass( "active" );
        $("#liDepartmentReport").addClass( "active" );
        $("#liExamListReport").removeClass( "active" );
        $("#liCompanyReport").removeClass( "active" );
        $("#liAllCompanyReport").removeClass( "active" );
        $("#divProbationerReport").hide();
        $("#divDepartmentReport").show();
        $("#divExamListReport").hide();
        $("#divCompanyReport").hide();
        $("#divAllCompanyReport").hide();
        window.localStorage.setItem("tab", "departmentReport")
    });

    $("#aExamListReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").removeClass( "active" );
        $("#liDepartmentReport").removeClass( "active" );
        $("#liExamListReport").addClass( "active" );
        $("#liCompanyReport").removeClass( "active" );
        $("#liAllCompanyReport").removeClass( "active" );
        $("#divProbationerReport").hide();
        $("#divDepartmentReport").hide();
        $("#divExamListReport").show();
        $("#divCompanyReport").hide();
        $("#divAllCompanyReport").hide();
        window.localStorage.setItem("tab", "examListReport")
    });

    $("#aCompanyReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").removeClass( "active" );
        $("#liDepartmentReport").removeClass( "active" );
        $("#liExamListReport").removeClass( "active" );
        $("#liCompanyReport").addClass( "active" );
        $("#liAllCompanyReport").removeClass( "active" );
        $("#divProbationerReport").hide();
        $("#divDepartmentReport").hide();
        $("#divExamListReport").hide();
        $("#divCompanyReport").show();
        $("#divAllCompanyReport").hide();
        window.localStorage.setItem("tab", "companyReport")
    });

    $("#aAllCompanyReport").click(function(e) {
        e.preventDefault();
        $("#liProbationerReport").removeClass( "active" );
        $("#liDepartmentReport").removeClass( "active" );
        $("#liExamListReport").removeClass( "active" );
        $("#liCompanyReport").removeClass( "active" );
        $("#liAllCompanyReport").addClass( "active" );
        $("#divProbationerReport").hide();
        $("#divDepartmentReport").hide();
        $("#divExamListReport").hide();
        $("#divCompanyReport").hide();
        $("#divAllCompanyReport").show();
        window.localStorage.setItem("tab", "allCompanyReport")
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