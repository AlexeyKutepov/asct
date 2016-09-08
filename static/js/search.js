/**
 * Created by alexey on 05.09.16.
 */
$(document).ready(function () {

    /**
     * Поиск по таблице пользователей
     */
    var userSearch = function () {
        $('#tableUserList > tbody > tr').each(function () {
            if (($(this).find('a').html().toUpperCase()).indexOf($("#inputUserSearch").val().toUpperCase()) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    };

    $("#buttonUserSearch").click(userSearch);
    $("#inputUserSearch").change(userSearch).keyup(userSearch);

    /**
     * Поиск по таблице уволенных сотрудников
     */
    var fireUserSearch = function() {
        $('#tableFireUserList > tbody > tr').each(function() {
            if(($(this).find('a').html().toUpperCase()).indexOf($("#inputFireUserSearch").val().toUpperCase()) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    };

    $("#buttonFireUserSearch").click(fireUserSearch);
    $("#inputFireUserSearch").change(fireUserSearch).keyup(fireUserSearch);

    /**
     * Поиск по таблице с учебными программами
     */
    var journalSearch = function() {
        $('#tableJournalList > tbody > tr').each(function() {
            if(($(this).find('a').html().toUpperCase()).indexOf($("#inputJournalSearch").val().toUpperCase()) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    };

    $("#buttonJournalSearch").click(journalSearch);
    $("#inputJournalSearch").change(journalSearch).keyup(journalSearch);

    /**
     * Поиск по таблице компаний
     */
    var companySearch = function() {
        $('#tableCompanyList > tbody > tr').each(function() {
            if(($(this).find('a').html().toUpperCase()).indexOf($("#inputCompanySearch").val().toUpperCase()) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    };

    $("#buttonCompanySearch").click(companySearch);
    $("#inputCompanySearch").change(companySearch).keyup(companySearch);

    /**
     * Поиск по таблице должностей
     */
    var positiontSearch = function() {
        $('#tablePositionList > tbody > tr').each(function() {
            if(($(this).find("td:first").html().toUpperCase()).indexOf($("#inputPositionSearch").val().toUpperCase()) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    };

    $("#buttonPositionSearch").click(positiontSearch);
    $("#inputPositionSearch").change(positiontSearch).keyup(positiontSearch);

});

