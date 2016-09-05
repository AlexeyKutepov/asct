/**
 * Created by alexey on 05.09.16.
 */
$(document).ready(function () {
    $.ajax({
        type: "POST",
        url: "/get/journal/list/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function (data) {
            $("#tableJournalList > tbody > tr").each(function () {
                $(this).remove();
            });
            var journalList = data["journal_list"];
            var result = "";
            for (var i = 0; i < journalList.length; i++) {
                result += "<tr><td><a href=\"/journal/settings/" + journalList[i]["id"] + "/\" name=\"aJournal\" property=\"" + journalList[i]["id"] + "\">" + journalList[i]["name"] + "</a></td><td>" + journalList[i]["company"] + "</td></tr>";
            }
            $("#tableJournalList").append(result);
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log("Error: " + errorThrown + xhr.status + xhr.responseText);
        }
    });
});