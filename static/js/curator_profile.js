$(document).ready(function () {

    var userSearch = function() {
        $('#tableUserList > tbody > tr').each(function() {
            if(($(this).find('a').html()).indexOf($("#inputUserSearch").val())) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    };

    $("#buttonUserSearch").click(userSearch);
    $("#inputUserSearch").change(userSearch).keyup(userSearch);


    $.ajax({
        type: "POST",
        url: "/get/journal/list/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            id: $( this).attr("property")
        },
        success: function(data) {
            $("#tableJournalList > tbody > tr").each(function() {
                $(this).remove();
            });
            var journalList = data["journal_list"];
            var result = "";
            for (var i = 0; i < journalList.length; i++) {
                result += "<tr><td><a href=\"journal/settings/" + journalList[i]["id"] + "/\" name=\"aJournal\" property=\"" + journalList[i]["id"] + "\">" + journalList[i]["name"] + "</a></td><td>" + journalList[i]["owner"] + "</td></tr>";
            }
            $("#tableJournalList").append(result);
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });


    $("a[name='aCompanyName']").click(function() {
        $.ajax({
            type: "POST",
            url: "/get/department/list/",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                id: $( this).attr("property")
            },
            success: function(data) {
                $("#tableDepartmentList > tbody > tr").each(function() {
                    $(this).remove();
                });
                var departmentList = data["department_list"];
                var result = "";
                for (var i = 0; i < departmentList.length; i++) {
                    result += "<tr><td><a href=\"#\" name=\"aDepartmentName\" property=\"" + departmentList[i]["id"] + "\">" + departmentList[i]["name"] + "</a></td></tr>";
                }
                $("#tableDepartmentList").append(result);
            },
            error: function(xhr, textStatus, errorThrown) {
                alert("Error: "+errorThrown+xhr.status+xhr.responseText);
            }
        });
        return false;
    });


    $('#tableDepartmentList').on( "click", "a[name='aDepartmentName']", function() {
        $.ajax({
            type: "POST",
            url: "/get/user/list/by/department/",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                id: $( this).attr("property")
            },
            success: function(data) {
                $("#tableUserList > tbody > tr").each(function() {
                    $(this).remove();
                });
                var userList = data["user_list"];
                var result = "";
                for (var i = 0; i < userList.length; i++) {
                    result += "<tr><td><a href=\"/accounts/settings/" + userList[i]["id"] + "\" property=\"" + userList[i]["id"] + "\">" + userList[i]["name"] + "</a></td></tr>";
                }
                $("#tableUserList").append(result);
            },
            error: function(xhr, textStatus, errorThrown) {
                alert("Error: "+errorThrown+xhr.status+xhr.responseText);
            }
        });
        return false;
    });

});

