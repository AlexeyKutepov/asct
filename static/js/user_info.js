$(document).ready(function () {

    $.ajax({
        type: "POST",
        url: "/get/theme/list/by/user/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            id: $("#userId").val()
        },
        success: function(data) {
            $("#tableUserStatisticList > tbody > tr").each(function() {
                $(this).remove();
            });
            var userStatisticList = data["user_statistic_list"];
            var result = "";
            for (var i = 0; i < userStatisticList.length; i++) {
                result +=
                    "<tr>" +
                        "<td><a href=\"/theme/settings/" + userStatisticList[i]["id"] + "/\">" + userStatisticList[i]["name"] +"</a></td>" +
                        "<td>" + userStatisticList[i]["status"] +"</td>" +
                        "<td>" + userStatisticList[i]["date_from"] +"</td>" +
                        "<td>" + userStatisticList[i]["date_to"] +"</td>" +
                        "<td>" +
                            "<div class=\"progress\"><div class=\"progress-bar\" role=\"progressbar\" aria-valuenow=\"" + userStatisticList[i]["progress"] + "\" aria-valuemin=\"0\" aria-valuemax=\"100\" style=\"width: " + userStatisticList[i]["progress"] + "%;\"><span class=\"sr-only\">" + userStatisticList[i]["progress"] + "% Complete</span></div></div>" +
                        "</td>" +
                        "<td></td>" +
                    "</tr>";
            }
            $("#tableUserStatisticList").append(result);
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });

    $.ajax({
        type: "POST",
        url: "/get/journal/list/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            id: $( this).attr("property")
        },
        success: function(data) {
            $('#selectJournal')
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
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });

});

