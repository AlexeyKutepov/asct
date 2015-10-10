$(document).ready(function () {

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

});

