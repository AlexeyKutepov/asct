$(document).ready(function () {

//    $.ajax({
//        type: "POST",
//        url: "/get/user/list/by/theme/",
//        data: {
//            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
//            id: $("#themeId").val()
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
//                        "<td><a href=\"/user/info/" + userStatisticList[i]["id"] + "/\">" + userStatisticList[i]["fio"] +"</a></td>" +
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

