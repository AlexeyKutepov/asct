$(document).ready(function () {
    if (supports_html5_storage) {
        var tab = window.localStorage.getItem("tab");
        if (tab == "exam") {
            $("#liStudy").removeClass( "active" );
            $("#liTest").removeClass( "active" );
            $("#liExam").addClass( "active" );
            $("#divStudy").hide();
            $("#divTest").hide();
            $("#divExam").show();
        } else if (tab == "test") {
            $("#liStudy").removeClass( "active" );
            $("#liTest").addClass( "active" );
            $("#liExam").removeClass( "active" );
            $("#divStudy").hide();
            $("#divTest").show();
            $("#divExam").hide();
        }
    }

    $("#aStudy").click(function(e) {
        e.preventDefault();
        $("#liStudy").addClass( "active" );
        $("#liExam").removeClass( "active" );
        $("#liTest").removeClass( "active" );
        $("#divStudy").show();
        $("#divExam").hide();
        $("#divTest").hide();
        window.localStorage.setItem("tab", "study")
    });

    $("#aExam").click(function(e) {
        e.preventDefault();
        $("#liStudy").removeClass( "active" );
        $("#liTest").removeClass( "active" );
        $("#liExam").addClass( "active" );
        $("#divStudy").hide();
        $("#divTest").hide();
        $("#divExam").show();
        window.localStorage.setItem("tab", "exam")
    });

    $("#aTest").click(function(e) {
        e.preventDefault();
        $("#liStudy").removeClass( "active" );
        $("#liTest").addClass( "active" );
        $("#liExam").removeClass( "active" );
        $("#divStudy").hide();
        $("#divTest").show();
        $("#divExam").hide();
        window.localStorage.setItem("tab", "test")
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
            $('#selectJournalTest')
                .find('option')
                .remove()
                .end()
                .selectpicker('refresh')
            ;
            var journalList = data["journal_list"];
            for (var i = 0; i < journalList.length; i++) {
                $('#selectJournal').append($("<option/>", {
                    value: journalList[i]["id"],
                    text: journalList[i]["name"]
                })).selectpicker('refresh');
                $('#selectExamJournal').append($("<option/>", {
                    value: journalList[i]["id"],
                    text: journalList[i]["name"]
                })).selectpicker('refresh');
                $('#selectJournalTest').append($("<option/>", {
                    value: journalList[i]["id"],
                    text: journalList[i]["name"]
                })).selectpicker('refresh');
            }
            $("#selectJournal").trigger( "change" );
            $("#selectExamJournal").trigger( "change" );
            $("#selectJournalTest").trigger( "change" );
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

     $("#selectJournalTest").change(function() {
        $.ajax({
            type: "POST",
            url: "/get/test/list/by/journal/",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                id: $(this).val()
            },
            success: function (data) {
                $('#selectTest')
                    .find('option')
                    .remove()
                    .end()
                    .selectpicker('refresh')
                ;
                var testList = data["test_list"];
                for (var i = 0; i < testList.length; i++) {
                    $('#selectTest').append($("<option/>", {
                        value: testList[i]["id"],
                        text: testList[i]["name"]
                    })).selectpicker('refresh');
                }
                if (testList.length > 0) {
                    $("#formScheduleTest").attr('action', '/exam/schedule/test/to/user/');
                }
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


$(function () {
    $('div[id^="datepicker"]').datetimepicker({
                format: 'DD.MM.YYYY',
                locale: 'ru'
            });
});

$(function () {
    $('div[id^="datetimepicker"]').datetimepicker({
                locale: 'ru'
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

