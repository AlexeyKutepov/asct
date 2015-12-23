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

    $.ajax({
        type: "POST",
        url: "/get/probationer/list/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            themeId: document.getElementById('themeId').value
        },
        success: function(data) {
            $('#selectProbationer')
                .find('option')
                .remove()
                .end()
                .selectpicker('refresh')
            ;
            $('#selectExamProbationer')
                .find('option')
                .remove()
                .end()
                .selectpicker('refresh')
            ;
            var probationerList = data["probationer_list"];
            for (var i = 0; i < probationerList.length; i++) {
                $('#selectProbationer').append($("<option/>", {
                    value: probationerList[i]["id"],
                    text: probationerList[i]["name"]
                })).selectpicker('refresh');
                $('#selectExamProbationer').append($("<option/>", {
                    value: probationerList[i]["id"],
                    text: probationerList[i]["name"]
                })).selectpicker('refresh');
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });

    $.ajax({
        type: "POST",
        url: "/get/examiner/list/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            themeId: document.getElementById('themeId').value
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
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });

    $("#aStudy").click(function(e) {
        e.preventDefault();
        $("#liStudy").addClass( "active" );
        $("#liExam").removeClass( "active" );
        $("#divStudy").show();
        $("#divExam").hide();
        window.localStorage.setItem("tab", "study")
    });

    $("#aExam").click(function(e) {
        e.preventDefault();
        $("#liStudy").removeClass( "active" );
        $("#liExam").addClass( "active" );
        $("#divStudy").hide();
        $("#divExam").show();
        window.localStorage.setItem("tab", "exam")
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

function downloadFile(id) {
    $.ajax({
        type: "POST",
        url: "/download/file/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            id: id
        },
        success: function(data) {
            return data;
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
}

