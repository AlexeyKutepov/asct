$(document).ready(function () {

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


