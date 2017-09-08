$(document).ready(function () {
    $('#auth-button').click(function() {
        var data = {};
        $('#auth-error').text('\n');
        $('#authentication input').each(function() {
            if ($(this).hasClass('inputfield')) {
                data[$(this).attr('name')] = $(this).val();
            }
            else if($(this).attr('name') == 'csrfmiddlewaretoken') {
                data[$(this).attr('name')] = $(this).val();
            }
        });
        if (data['username'] == '') {
            $('#auth-error').text('Please enter your username');
            return;
        }
        if (data['password'] == '') {
            $('#auth-error').text('Please enter your password');
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
                    location.reload();
                    // $('#auth-error').text('\n');
                    Flash.clear();
                }
                else {
                    // $('#auth-error').text(data['msg']);
                    Flash.error(data['msg']);
                }
            },
            error: function() {
                // $('#auth-error').text('A problem occured on the server.');
                Flash.error('A problem occurred on the server.');
            }
        });
    });

    $('#reg-button').click(function() {
        var data = {};
        var err = false;

        $('#reg-user-error').text(' ');
        $('#reg-email-error').text(' ');
        $('#reg-pass-error').text(' ');
        $('#reg-confirm-error').text(' ');
        $('#registration input').each(function() {
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
            url: '/account/register',
            data: data,
            success: function(data) {
                console.log(data);
                if ('' in data) {
                    location.reload();
                }
                else {
                    for (key in data)
                    {
                        $('#' + key).text(data[key]);
                    }
                }
            },
            error: function() {
                // $('#reg-confirm-error').text('A problem occured on the server.');
                Flash.error('A problem occurred on the server.');
            }
        });
    });
});
