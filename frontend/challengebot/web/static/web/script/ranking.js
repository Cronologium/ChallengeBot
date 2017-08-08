$(document).ready(function() {
    var pos_start = parseInt($('#position').val());
    if ($("#current-game").val() == "None")
    {
        $("#current-game").val("");
    }
    $('#game-select').val($("#current-game").val());
    $('.pos').each(function(position) {
        $(this).text('#' + String(pos_start));
        var ranking_row = $('#ranking-table tr').eq(position + 1);
        if (pos_start == 1)
        {
            ranking_row.css('font-size', 30);
            ranking_row.css("background-color", "rgba(255,215,0,0.5)");
        }
        if (pos_start == 2)
        {
            ranking_row.css('font-size', 22);
            ranking_row.css("background-color", "rgba(192,192,192,0.5)");
        }
        if (pos_start == 3)
        {
            ranking_row.css('font-size', 15);
            ranking_row.css("background-color", "rgba(205,127,50,0.5)");
        }
        pos_start += 1;
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