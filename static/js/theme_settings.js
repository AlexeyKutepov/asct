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

    $.ajax({
        type: "POST",
        url: "/get/probationer/list/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function(data) {
            $('#selectProbationer')
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
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });

});

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

