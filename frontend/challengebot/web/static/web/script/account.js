$(document).ready(function () {
    $('#auth-button').click(function() {
        var data = {};
        $('#authentication input').each(function() {
            if ($(this).hasClass('inputfield')) {
                data[$(this).attr('name')] = $(this).val();
            }
            else if($(this).attr('name') == 'csrfmiddlewaretoken') {
                data[$(this).attr('name')] = $(this).val();
            }
        });
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: '/account/login',
            data: data,
            success: function(data) {
                if (data['msg'] == 'success') {
                    window.location = '/';
                }
                else {
                    $('#auth-error').text(data['msg']);
                }
            },
            error: function() {
                $('#auth-error').text('A problem occured on the server.');
            }
        });
    });
    $('#reg-button').click(function() {

    });
});
