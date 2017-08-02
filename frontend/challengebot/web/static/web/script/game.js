$(document).ready(function () {
    var elem = document.getElementById("id_your_code");
    var editor = CodeMirror.fromTextArea(elem, {mode: "text/x-python", lineNumbers: true, theme: "material", tabSize: 4, indentUnit: 4, matchBrackets: true});
    editor.setSize("100%", "500px");
    function setLanguage() {
        if ($("#id_language option:selected").val() == "PY2" || $("#id_language option:selected").val() == "PY3") {
            editor.setOption("mode", "text/x-python");
            editor.getDoc().setValue($("#python-code").text());
        }
        if ($("#id_language option:selected").val() == "Cpp") {
            editor.setOption("mode", "text/x-c++src");
            editor.getDoc().setValue($("#cpp-code").text());
        }
    }
    $("#id_language").change(setLanguage);
    setLanguage();

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