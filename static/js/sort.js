/**
 * Created by alexey on 05.09.16.
 */
$(document).ready(function () {

    /**
     * Сортировка таблицы списка пользователей
     */
    var tableUserList = $("#tableUserList");

    $('#thUserName, #thUserPosition, #thUserCompany, #thUserType')
        .wrapInner('<span title="sort this column"/>')
        .each(function () {
            var th = $(this),
                thIndex = th.index(),
                inverse = false;
            th.click(function () {
                tableUserList.find('td').filter(function () {
                    return $(this).index() === thIndex;
                }).sortElements(function (a, b) {
                    if ($.text([a]) == $.text([b]))
                        return 0;
                    return $.text([a]) > $.text([b]) ?
                        inverse ? -1 : 1
                        : inverse ? 1 : -1;
                }, function () {
                    // parentNode is the element we want to move
                    return this.parentNode;
                });
                inverse = !inverse;
            });
        });


    /**
     * Сортировка таблицы уволенных сотрудников
     */
    var tableFireUserList = $("#tableFireUserList");

    $('#thFireUserName, #thFireUserPosition, #thFireUserCompany, #thFireUserType')
        .wrapInner('<span title="sort this column"/>')
        .each(function(){
        var th = $(this),
            thIndex = th.index(),
            inverse = false;
        th.click(function(){
            tableFireUserList.find('td').filter(function(){
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

    /**
     * Сортировка таблицы со списком учебных программ
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

});