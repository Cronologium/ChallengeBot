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
            FlashService.error('auth-error', 'Please enter your username');
            return;
        }
        if (data['password'] == '') {
            FlashService.error('auth-error', 'Please enter your password');
            return;
        }
        if (data['csrfmiddlewaretoken'] == '') {
            FlashService.error('auth-error', 'No login token!');
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
                    FlashService.clear('flash-container');
                }
                else {
                    FlashService.error('auth-error', data['msg']);
                }
            },
            error: function() {
                FlashService.error('auth-error', 'A problem occurred on the server.');
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
                        console.log(key);
                        FlashService.error(key, data[key]);
                    }
                }
            },
            error: function() {
                FlashService.error('reg-confirm-error', 'A problem occurred on the server');
            }
        });
    });
});
