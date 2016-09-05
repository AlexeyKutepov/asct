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

});

