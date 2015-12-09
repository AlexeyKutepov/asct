$(document).ready(function () {

    $("#aStudy").click(function() {
        $("#liStudy").addClass( "active" );
        $("#liExam").removeClass( "active" );
        $("#liTest").removeClass( "active" );
        $("#divTest").hide();
        $("#divStudy").show();
        $("#divExam").hide();
    });

    $("#aExam").click(function() {
        $("#liStudy").removeClass( "active" );
        $("#liExam").addClass( "active" );
        $("#liTest").removeClass( "active" );
        $("#divTest").hide();
        $("#divStudy").hide();
        $("#divExam").show();
    });

    $("#aTest").click(function() {
        $("#liStudy").removeClass( "active" );
        $("#liExam").removeClass( "active" );
        $("#liTest").addClass( "active" );
        $("#divTest").show();
        $("#divStudy").hide();
        $("#divExam").hide();
    });

});

