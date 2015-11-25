$(document).ready(function () {
    if (supports_html5_storage) {
        var tab = window.localStorage.getItem("tab");
        if (tab == "exam") {
            $("#liStudy").removeClass( "active" );
            $("#liExam").addClass( "active" );
            $("#divStudy").hide();
            $("#divExam").show();
        }
    }

    $("#aStudy").click(function() {
        $("#liStudy").addClass( "active" );
        $("#liExam").removeClass( "active" );
        $("#divStudy").show();
        $("#divExam").hide();
        window.localStorage.setItem("tab", "study")
    });

    $("#aExam").click(function() {
        $("#liStudy").removeClass( "active" );
        $("#liExam").addClass( "active" );
        $("#divStudy").hide();
        $("#divExam").show();
        window.localStorage.setItem("tab", "exam")
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

