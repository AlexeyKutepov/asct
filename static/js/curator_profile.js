$(document).ready(function () {

    var curatorSearch = function() {
        $('#tableCuratorList > tbody > tr').each(function() {
            if(($(this).find('a').html()).indexOf($("#inputCuratorSearch").val())) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    };

    $("#buttonCuratorSearch").click(curatorSearch);
    $("#inputCuratorSearch").change(curatorSearch).keyup(curatorSearch);

    var adminSearch = function() {
        $('#tableAdminList > tbody > tr').each(function() {
            if(($(this).find('a').html()).indexOf($("#inputAdminSearch").val())) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    };

    $("#buttonAdminSearch").click(adminSearch);
    $("#inputAdminSearch").change(adminSearch).keyup(adminSearch);

    var operatorSearch = function() {
        $('#tableOperatorList > tbody > tr').each(function() {
            if(($(this).find('a').html()).indexOf($("#inputOperatorSearch").val())) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    };

    $("#buttonOperatorSearch").click(operatorSearch);
    $("#inputOperatorSearch").change(operatorSearch).keyup(operatorSearch);

    var probationerSearch = function() {
        $('#tableProbationerList > tbody > tr').each(function() {
            if(($(this).find('a').html()).indexOf($("#inputProbationerSearch").val())) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    };

    $("#buttonProbationerSearch").click(probationerSearch);
    $("#inputProbationerSearch").change(probationerSearch).keyup(probationerSearch);


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
    });

});

