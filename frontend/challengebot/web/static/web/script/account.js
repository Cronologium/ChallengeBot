$(document).ready(function () {
    $('#auth-button').click(function() {
        var data = {};
        $('#auth-error').text(' ');
        $('#authentication input').each(function() {
            if ($(this).hasClass('inputfield')) {
                data[$(this).attr('name')] = $(this).val();
            }
            else if($(this).attr('name') == 'csrfmiddlewaretoken') {
                data[$(this).attr('name')] = $(this).val();
            }
        });
        if (data['username'] == '') {
            $('#auth-error').text('Please fill out the username form');
            return;
        }
        if (data['password'] == '') {
            $('#auth-error').text('Please fill out the password form');
            return;
        }
        if (data['csrfmiddlewaretoken'] == '') {
            $('#auth-error').text('No login token!');
            return;
        }
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: '/account/login',
            data: data,
            success: function(data) {
                if (data['msg'] == 'success') {
                    window.location = '/';
                    $('#auth-error').text(' ');
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
