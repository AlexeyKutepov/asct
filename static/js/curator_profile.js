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

    var journalSearch = function() {
        $('#tableJournalList > tbody > tr').each(function() {
            if(($(this).find('a').html()).indexOf($("#inputJournalSearch").val())) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    };

    $("#buttonJournalSearch").click(journalSearch);
    $("#inputJournalSearch").change(journalSearch).keyup(journalSearch);

    var companySearch = function() {
        $('#tableCompanyList > tbody > tr').each(function() {
            if(($(this).find('a').html()).indexOf($("#inputCompanySearch").val())) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    };

    $("#buttonCompanySearch").click(companySearch);
    $("#inputCompanySearch").change(companySearch).keyup(companySearch);

    var positiontSearch = function() {
        $('#tablePositionList > tbody > tr').each(function() {
            if(($(this).find("td:first").html()).indexOf($("#inputPositionSearch").val())) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    };

    $("#buttonPositionSearch").click(positiontSearch);
    $("#inputPositionSearch").change(positiontSearch).keyup(positiontSearch);

    var departmentSearch = function() {
        $('#tableDepartmentList > tbody > tr').each(function() {
            if(($(this).find('a').html()).indexOf($("#inputDepartmentSearch").val())) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    };

    $("#buttonDepartmentSearch").click(departmentSearch);
    $("#inputDepartmentSearch").change(departmentSearch).keyup(departmentSearch);

    var profilesSearch = function() {
        $('#tableProfileList > tbody > tr').each(function() {
            if(($(this).find('a').html()).indexOf($("#inputProfileSearch").val())) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    };

    $("#buttonProfileSearch").click(profilesSearch);
    $("#inputProfileSearch").change(profilesSearch).keyup(profilesSearch);

    $("#aShowAllUsers").click(function() {
        $(this).html("<i class=\"fa fa-check\"></i> Все пользователи");
        $("#aShowCurators").text("Кураторы");
        $("#aShowAdmins").text("Администраторы");
        $("#aShowOperators").text("Операторы");
        $("#aShowProbationers").text("Испытуемые");
        $('#tableUserList > tbody > tr').each(function() {
            $(this).show();
        });
        return false;
    });

    $("#aShowCurators").click(function() {
        $("#aShowAllUsers").text("Все пользователи");
        $(this).html("<i class=\"fa fa-check\"></i> Кураторы");
        $("#aShowAdmins").text("Администраторы");
        $("#aShowOperators").text("Операторы");
        $("#aShowProbationers").text("Испытуемые");
        $('#tableUserList > tbody > tr').each(function() {
            if($(this).find('input').attr("name") != "tdcurator") {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
        return false;
    });

    $("#aShowAdmins").click(function() {
        $("#aShowAllUsers").text("Все пользователи");
        $("#aShowCurators").text("Кураторы");
        $(this).html("<i class=\"fa fa-check\"></i> Администраторы");
        $("#aShowOperators").text("Операторы");
        $("#aShowProbationers").text("Испытуемые");
        $('#tableUserList > tbody > tr').each(function() {
            if($(this).find('input').attr("name") != "tdadmin") {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
        return false;
    });

    $("#aShowOperators").click(function() {
        $("#aShowAllUsers").text("Все пользователи");
        $("#aShowCurators").text("Кураторы");
        $("#aShowAdmins").text("Администраторы");
        $(this).html("<i class=\"fa fa-check\"></i> Операторы");
        $("#aShowProbationers").text("Испытуемые");
        $('#tableUserList > tbody > tr').each(function() {
            if($(this).find('input').attr("name") != "tdoperator") {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
        return false;
    });

    $("#aShowProbationers").click(function() {
        $("#aShowAllUsers").text("Все пользователи");
        $("#aShowCurators").text("Кураторы");
        $("#aShowAdmins").text("Администраторы");
        $("#aShowOperators").text("Операторы");
        $(this).html("<i class=\"fa fa-check\"></i> Испытуемые");
        $('#tableUserList > tbody > tr').each(function() {
            if($(this).find('input').attr("name") != "tdprobationer") {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
        return false;
    });


    $.ajax({
        type: "POST",
        url: "/get/journal/list/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function(data) {
            $("#tableJournalList > tbody > tr").each(function() {
                $(this).remove();
            });
            var journalList = data["journal_list"];
            var result = "";
            for (var i = 0; i < journalList.length; i++) {
                result += "<tr><td><a href=\"journal/settings/" + journalList[i]["id"] + "/\" name=\"aJournal\" property=\"" + journalList[i]["id"] + "\">" + journalList[i]["name"] + "</a></td><td>" + journalList[i]["company"] + "</td></tr>";
            }
            $("#tableJournalList").append(result);
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });

    /**
     * Сортировка таблиц
     */

    var tableJournalList = $("#tableJournalList");

    $('#thJournalName, #thJournalCompany')
        .wrapInner('<span title="sort this column"/>')
        .each(function(){
        var th = $(this),
            thIndex = th.index(),
            inverse = false;
        th.click(function(){
            tableJournalList.find('td').filter(function(){
                return $(this).index() === thIndex;
            }).sortElements(function(a, b){
                if( $.text([a]) == $.text([b]) )
                    return 0;
                return $.text([a]) > $.text([b]) ?
                    inverse ? -1 : 1
                    : inverse ? 1 : -1;
            }, function(){
                // parentNode is the element we want to move
                return this.parentNode;
            });
            inverse = !inverse;
        });
    });

    var tableUserList = $("#tableUserList");

    $('#thUserName, #thUserPosition, #thUserCompany, #thUserType')
        .wrapInner('<span title="sort this column"/>')
        .each(function(){
        var th = $(this),
            thIndex = th.index(),
            inverse = false;
        th.click(function(){
            tableUserList.find('td').filter(function(){
                return $(this).index() === thIndex;
            }).sortElements(function(a, b){
                if( $.text([a]) == $.text([b]) )
                    return 0;
                return $.text([a]) > $.text([b]) ?
                    inverse ? -1 : 1
                    : inverse ? 1 : -1;
            }, function(){
                // parentNode is the element we want to move
                return this.parentNode;
            });
            inverse = !inverse;
        });
    });

});

