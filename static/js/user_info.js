$(document).ready(function () {

//    $.ajax({
//        type: "POST",
//        url: "/get/theme/list/by/user/",
//        data: {
//            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
//            id: $("#userId").val()
//        },
//        success: function(data) {
//            $("#tableUserStatisticList > tbody > tr").each(function() {
//                $(this).remove();
//            });
//            var userStatisticList = data["user_statistic_list"];
//            var result = "";
//            for (var i = 0; i < userStatisticList.length; i++) {
//                result +=
//                    "<tr>" +
//                        "<td><a href=\"/theme/settings/" + userStatisticList[i]["id"] + "/\">" + userStatisticList[i]["name"] +"</a></td>" +
//                        "<td>" + userStatisticList[i]["status"] +"</td>" +
//                        "<td>" + userStatisticList[i]["date_from"].substring(0,10) +"</td>" +
//                        "<td>" + userStatisticList[i]["date_to"].substring(0,10) +"</td>" +
//                        "<td>" +
//                            "<div class=\"progress\"><div class=\"progress-bar\" role=\"progressbar\" aria-valuenow=\"" + userStatisticList[i]["progress"] + "\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: " + userStatisticList[i]["progress"] + "%;\"><span class=\"sr-only\">" + userStatisticList[i]["progress"] + "% Complete</span></div></div>" +
//                        "</td>" +
//                        "<td></td>" +
//                    "</tr>";
//            }
//            $("#tableUserStatisticList").append(result);
//        },
//        error: function(xhr, textStatus, errorThrown) {
//            console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
//        }
//    });

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

    $.ajax({
        type: "POST",
        url: "/get/journal/list/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            userId: document.getElementById('userId').value
        },
        success: function(data) {
            $('#selectJournal')
                .find('option')
                .remove()
                .end()
                .selectpicker('refresh')
            ;
            $('#selectExamJournal')
                .find('option')
                .remove()
                .end()
                .selectpicker('refresh')
            ;
            var journalList = data["journal_list"];
            for (var i = 0; i < journalList.length; i++) {
                var companyName = "";
                if (journalList[i]["company"]) {
                    companyName = " (" + journalList[i]["company"] + ")";
                }
                $('#selectJournal').append($("<option/>", {
                    value: journalList[i]["id"],
                    text: journalList[i]["name"] + companyName
                })).selectpicker('refresh');
                $('#selectExamJournal').append($("<option/>", {
                    value: journalList[i]["id"],
                    text: journalList[i]["name"] + companyName
                })).selectpicker('refresh');
            }
            $("#selectJournal").trigger( "change" );
            $("#selectExamJournal").trigger( "change" );
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });

    $("#selectJournal").change(function() {
        $.ajax({
            type: "POST",
            url: "/get/theme/list/by/journal/",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                id: $(this).val()
            },
            success: function (data) {
                $('#selectTheme')
                    .find('option')
                    .remove()
                    .end()
                    .selectpicker('refresh')
                ;
                var themeList = data["theme_list"];
                for (var i = 0; i < themeList.length; i++) {
                    $('#selectTheme').append($("<option/>", {
                        value: themeList[i]["id"],
                        text: themeList[i]["name"]
                    })).selectpicker('refresh');
                }
                if (themeList.length > 0) {
                    $("#formScheduleTheme").attr('action', '/schedule/theme/to/user/');
                }
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log("Error: " + errorThrown + xhr.status + xhr.responseText);
            }
        });
    });

    $("#selectExamJournal").change(function() {
        $.ajax({
            type: "POST",
            url: "/get/theme/list/by/journal/",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                id: $(this).val()
            },
            success: function (data) {
                $('#selectExamTheme')
                    .find('option')
                    .remove()
                    .end()
                    .selectpicker('refresh')
                ;
                var themeList = data["theme_list"];
                for (var i = 0; i < themeList.length; i++) {
                    $('#selectExamTheme').append($("<option/>", {
                        value: themeList[i]["id"],
                        text: themeList[i]["name"]
                    })).selectpicker('refresh');
                }
                if (themeList.length > 0) {
                    $("#formScheduleTheme").attr('action', '/schedule/theme/to/user/');
                }
                $("#selectExamTheme").trigger( "change" );
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log("Error: " + errorThrown + xhr.status + xhr.responseText);
            }
        });
    });

    $("#selectExamTheme").change(function() {
        var themeId =  $(this).val();
        $.ajax({
            type: "POST",
            url: "/get/examiner/list/",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                themeId: themeId
            },
            success: function(data) {
                $('#selectExaminer')
                    .find('option')
                    .remove()
                    .end()
                    .selectpicker('refresh')
                ;
                var examinerList = data["examiner_list"];
                for (var i = 0; i < examinerList.length; i++) {
                    $('#selectExaminer').append($("<option/>", {
                        value: examinerList[i]["id"],
                        text: examinerList[i]["name"]
                    })).selectpicker('refresh');
                }

                $("#formScheduleExam").attr('action', '/schedule/exam/'+themeId+'/' );

            },
            error: function(xhr, textStatus, errorThrown) {
                console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
            }
        });
    });

});

