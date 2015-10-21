/**
 * Created by Alexey Kutepov on 09.10.15.
 */

/**
 * Image preview
 * @param input
 */
function onPreview(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#impPreview').attr('src', e.target.result).width("200px").height("auto");
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$(document).ready(function () {
  $('.selectpicker').selectpicker({
      style: 'btn-default',
      size: 4
  });
});
