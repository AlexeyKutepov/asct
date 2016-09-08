$(document).ready(function () {
    /**
     * Переключение вкладок в окне компаний и должностей
     */
    if (supports_html5_storage) {
        var tabCompanyPosition = window.localStorage.getItem("tabCompanyPosition");
        if (tabCompanyPosition == "company") {
            $("#liCompanies").addClass("active");
            $("#liPositions").removeClass("active");
            $("#divCompanies").show();
            $("#divPositions").hide();
        } else if (tabCompanyPosition == "position") {
            $("#liCompanies").removeClass("active");
            $("#liPositions").addClass("active");
            $("#divCompanies").hide();
            $("#divPositions").show();
        }
    }

    $("#aCompanies").click(function (e) {
        e.preventDefault();
        $("#liCompanies").addClass("active");
        $("#liPositions").removeClass("active");
        $("#divCompanies").show();
        $("#divPositions").hide();
        window.localStorage.setItem("tabCompanyPosition", "company")
    });

    $("#aPositions").click(function (e) {
        e.preventDefault();
        $("#liCompanies").removeClass("active");
        $("#liPositions").addClass("active");
        $("#divCompanies").hide();
        $("#divPositions").show();
        window.localStorage.setItem("tabCompanyPosition", "position")
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