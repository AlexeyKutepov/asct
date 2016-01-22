$(document).ready(function () {

    $.ajax({
        type: "POST",
        url: "/get/probationer/list/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            testId: document.getElementById('testId').value
        },
        success: function(data) {
            $('#selectProbationer')
                .find('option')
                .remove()
                .end()
                .selectpicker('refresh')
            ;
            var probationerList = data["probationer_list"];
            for (var i = 0; i < probationerList.length; i++) {
                $('#selectProbationer').append($("<option/>", {
                    value: probationerList[i]["id"],
                    text: probationerList[i]["name"]
                })).selectpicker('refresh');

            }
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
});

$(function () {
    $('div[id^="datepicker"]').datetimepicker({
                format: 'DD.MM.YYYY',
                locale: 'ru'
            });
});
