$(document).ready(function () {
    if ($('#id_your_code').length > 0)
    {
        var elem = document.getElementById("id_your_code");
        var editor = CodeMirror.fromTextArea(elem, {mode: "text/x-python", lineNumbers: true, theme: 'liquibyte', tabSize: 4, indentUnit: 4, matchBrackets: true});
        editor.setSize("100%", "1200px");
        function setLanguage() {
            if ($("#id_language option:selected").val() == "PY") {
                editor.setOption("mode", "text/x-python");
                editor.getDoc().setValue($("#python-code").text());
            }
            if ($("#id_language option:selected").val() == "C") {
                editor.setOption("mode", "text/x-c++src");
                editor.getDoc().setValue($("#c-code").text());
            }
        }
        $("#id_language").change(setLanguage);
        setLanguage();
    }
    else
    {
        $('#game-data').css('width', '100%');
    }
    if ($('#xp-gain').length > 0)
    {
        var xp = $('#player-xp').val();
        var xp_reach = $('#reach-xp').val();
        if (xp_reach == -1)
        {
            $('#xp-gain').css("width", "100%");
        }
        $('#xp-gain').css("width", String(100.0 * xp / xp_reach) + "%");
        console.log(String(100.0 * xp / xp_reach) + "%");
    }
    $('#submission-submit').click(function() {
        var data = {}
        data['code'] = editor.getValue();
        data['language'] = $('#id_language').val();
        $('#submission-form input').each(function() {
            if($(this).attr('name') == 'csrfmiddlewaretoken') {
                data[$(this).attr('name')] = $(this).val();
            }
        });
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: '/submit/source/' + $('#game_id').val(),
            data: data,
            success: function(data) {
                if (data['msg'] == 'success') {
                    $('#submit-error').text('huh?');
                    window.location.replace('/jobs');
                }
                else {
                    $('#submit-error').text(data['msg']);
                }
            },
            error: function() {
                $('#submit-error').text('A problem occured on the server.');
            }
        });
    });

    $('#challenge-submit').click(function() {
        var data = {};
        data['selected_opponents'] = [];
        $("#id_selected_opponents > option").each(function(){
            data['selected_opponents'].push(this.value);
        });
        $('#challenge-form input').each(function() {
            if($(this).attr('name') == 'csrfmiddlewaretoken') {
                data[$(this).attr('name')] = $(this).val();
            }
        });
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: '/submit/challenge/' + $('#player_source_id').val(),
            data: data,
            success: function(data) {
                if (data['msg'] == 'success') {
                    $('#challenge-error').text('huh');
                    window.location.replace('/jobs');
                }
                else {
                    $('#challenge-error').text(data['msg']);
                }
            },
            error: function() {
                $('#challenge-error').text('A problem occured on the server.');
            }
        });
    });
});