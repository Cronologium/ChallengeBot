
$(document).ready(function() {
    var pos_start = parseInt($('#position').val());
    if ($("#current-game").val() == "None")
    {
        $("#current-game").val("");
    }
    $('#game-select').val($("#current-game").val());
    $('.pos').each(function(position) {
        $(this).text('#' + String(pos_start));
    });
    $('#game-select').change(function() {
        if ($('#game-select').find(':selected').val() != "")
        {
            window.location.replace('/ranking/' + $('#game-select').find(':selected').val());
        }
        else
        {
            window.location.replace('/ranking');
        }
    });
});