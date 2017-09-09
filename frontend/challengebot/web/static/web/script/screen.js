$( document ).ready(function() {
    var data_rows = null;
    var crt_data = 1;
    function create_table() {
        data_rows = $('#data p');
        var limits = data_rows.eq(0).text().split("|")[0].split(" ");
        var start_data = data_rows.eq(0).text().split("|")[1].split(" ");
        var txt = data_rows.eq(0).text().split("|")[2]
        var img = start_data[2];
        var px_w = parseInt(limits[0]);
        var px_h = parseInt(limits[1]);
        var w = parseInt(limits[2]);
        var h = parseInt(limits[3]);
        var table_data = '';
        for (var i = 0; i < h; ++i) {
            table_data += '<tr class="cell-row">'
            for (var j = 0; j < w; ++j)
            {
                table_data += '<td class="cell-data" id="c' + i + '_' + j + '"></td>';
            }
            table_data += '</tr>'
        }
        $('#screen-pixels').append(table_data);
        $('.cell-data').each(function() {
            $(this).css('width', px_w);
            $(this).css('height', px_h);
            $(this).css('background-image', "url(/static/web/style/res/" + img);
        });

        $('#screen-text').append(txt);
        for (var i = 3; i < data_rows.eq(0).text().split("|").length; ++i)
        {
            var cell = data_rows.eq(0).text().split("|")[i].trim();
            var x = cell.split(" ")[0];
            var y = cell.split(" ")[1];
            var value = cell.split(" ")[3];
            $('#c' + x + '_' + y).css('background-image', "url(/static/web/style/res/" + value);
        }
    };


    function next() {
        if (crt_data < data_rows.length)
        {
            var d = data_rows.eq(crt_data).text().split("|");
            for (i in d) {
                var cell = d[i].trim();
                var x = cell.split(" ")[0];
                var y = cell.split(" ")[1];
                var value = cell.split(" ")[3];
                $('#c' + x + '_' + y).css('background-image', "url(/static/web/style/res/" + value);
            }
            crt_data += 1;
        }
        if (crt_data == data_rows.length)
        {
            $('#nextButton').prop("disabled", true);
        }
        $('#prevButton').prop("disabled", false);
    }
    function prev() {
        if (crt_data > 1)
        {
            crt_data -= 1;
            var d = data_rows.eq(crt_data).text().split("|");
            for (i in d) {
                var cell = d[i].trim();
                var x = cell.split(" ")[0];
                var y = cell.split(" ")[1];
                var value = cell.split(" ")[2];
                $('#c' + x + '_' + y).css('background-image', "url(/static/web/style/res/" + value);
            }
        }
        if (crt_data == 1)
        {
            $('#prevButton').prop("disabled", true);
        }
        $('#nextButton').prop("disabled", false);
    }
    function autoplay(){
        isStopCommand = false;
        playLoop();
    }

    var isStopCommand = false;

    function isNumber(n) {
        return !isNaN(parseFloat(n)) && isFinite(n);
    }

    function playLoop(){
        if ($("#nextButton").prop("disabled") != true && !isStopCommand){
            var delay = $("#autoInterval").val();
            if (delay == '' || !isNumber(delay)){
                alert("Please set the play interval (in milliseconds)!");
                return;
            }
            var intdelay = parseInt(delay);
            next();
            setTimeout(function() { playLoop(); }, intdelay);
        }
    }

    function stop(){
        isStopCommand = true;
    }

    function last(){
        while ($("#nextButton").prop("disabled") != true){
            next();
        }
    }

    function first(){
        while ($("#prevButton").prop("disabled") != true){
            prev();
        }
    }

    $('#nextButton').click(next);
    $('#prevButton').click(prev);
    $('#firstButton').click(first);
    $('#lastButton').click(last);
    $('#stopButton').click(stop);
    $('#autoButton').click(playLoop);
    create_table();

});