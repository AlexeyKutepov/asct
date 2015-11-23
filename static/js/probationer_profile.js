$(document).ready(function () {

    $("#aStudy").click(function() {
        $("#liStudy").addClass( "active" );
        $("#liExam").removeClass( "active" );
        $("#divStudy").show();
        $("#divExam").hide();
    });

    $("#aExam").click(function() {
        $("#liStudy").removeClass( "active" );
        $("#liExam").addClass( "active" );
        $("#divStudy").hide();
        $("#divExam").show();
    });

});

