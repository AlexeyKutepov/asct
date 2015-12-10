$(document).ready(function () {

    if (supports_html5_storage) {
        var tab = window.localStorage.getItem("tab");
        if (tab == "exam") {
            $("#liStudy").removeClass( "active" );
            $("#liTest").removeClass( "active" );
            $("#liExam").addClass( "active" );
            $("#divTest").hide();
            $("#divStudy").hide();
            $("#divExam").show();
        } else if (tab == "test") {
            $("#liStudy").removeClass( "active" );
            $("#liExam").removeClass( "active" );
            $("#liTest").addClass( "active" );
            $("#divTest").show();
            $("#divStudy").hide();
            $("#divExam").hide();
        }
    }

    $("#aStudy").click(function() {
        $("#liStudy").addClass( "active" );
        $("#liExam").removeClass( "active" );
        $("#liTest").removeClass( "active" );
        $("#divTest").hide();
        $("#divStudy").show();
        $("#divExam").hide();
        window.localStorage.setItem("tab", "study")
    });

    $("#aExam").click(function() {
        $("#liStudy").removeClass( "active" );
        $("#liExam").addClass( "active" );
        $("#liTest").removeClass( "active" );
        $("#divTest").hide();
        $("#divStudy").hide();
        $("#divExam").show();
        window.localStorage.setItem("tab", "exam")
    });

    $("#aTest").click(function() {
        $("#liStudy").removeClass( "active" );
        $("#liExam").removeClass( "active" );
        $("#liTest").addClass( "active" );
        $("#divTest").show();
        $("#divStudy").hide();
        $("#divExam").hide();
        window.localStorage.setItem("tab", "test")
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

