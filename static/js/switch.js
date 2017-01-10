$(document).ready(function () {
    /**
     * Переключение вкладок в окне компаний и должностей
     */
    if (supports_html5_storage) {
        var tabDepartmentPosition = window.localStorage.getItem("tabDepartmentPosition");
        if (tabDepartmentPosition == "department") {
            $("#liDepartments").addClass("active");
            $("#liPositions").removeClass("active");
            $("#divDepartments").show();
            $("#divPositions").hide();
        } else if (tabDepartmentPosition == "position") {
            $("#liDepartments").removeClass("active");
            $("#liPositions").addClass("active");
            $("#divDepartments").hide();
            $("#divPositions").show();
        }
    }

    $("#aDepartments").click(function (e) {
        e.preventDefault();
        $("#liDepartments").addClass("active");
        $("#liPositions").removeClass("active");
        $("#divDepartments").show();
        $("#divPositions").hide();
        window.localStorage.setItem("tabDepartmentPosition", "department")
    });

    $("#aPositions").click(function (e) {
        e.preventDefault();
        $("#liDepartments").removeClass("active");
        $("#liPositions").addClass("active");
        $("#divDepartments").hide();
        $("#divPositions").show();
        window.localStorage.setItem("tabDepartmentPosition", "position")
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