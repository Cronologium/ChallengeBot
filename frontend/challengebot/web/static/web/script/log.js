var p1_original_values = [];
var p2_original_values = [];
$( document ).ready(function() {
    $('#current_shooter').html("It's " + $('#player1').val() + "'s turn to shoot.");
    $('#prevButton').prop("disabled", true);

    $('#p1_caption').text($('#player1').val() + "'s battlefield:");
    $('#p2_caption').text($('#player2').val() + "'s battlefield:");

    $('[name="1_block"]').each(function(index){
        $(this).attr('id', '1_' + index);
        $(this).css('background-image', "url(/static/web/style/res/water_block.jpg)");
        p1_original_values[index] = 'url(/static/web/style/res/water_block.jpg)';
    });
    $('[name="2_block"]').each(function(index){
        $(this).attr('id', '2_' + index);
        $(this).css('background-image', "url(/static/web/style/res/water_block.jpg)");
        p2_original_values[index] = 'url(/static/web/style/res/water_block.jpg)';
    });

    var p1_ships = $('#player1').val() + "_ship";
    $("[name="+p1_ships+"]").each(function(index){
        var coordinates = [];
        $(this).children().each(function(iindex){
            coordinates.push($(this).html());
        });
        x1 = parseInt(coordinates[0]);
        y1 = parseInt(coordinates[1]);
        x2 = parseInt(coordinates[2]);
        y2 = parseInt(coordinates[3]);
        if (y1 == y2){
            if (x1 <= x2){
                for (var i = x1; i <= x2; ++i){
                    var block_id = i * 10 + y1;
                    var img = 'none';
                    if (x2 == x1){
                        img = 'url(/static/web/style/res/ship1_1.png)';
                    }
                    else if (x2 - x1 == 1){
                        img = 'url(/static/web/style/res/ship2_' + (i - x1 + 1) + 'v.png)';
                    }
                    else if (x2 - x1 == 2){
                        img = 'url(/static/web/style/res/ship3_' + (i - x1 + 1) + 'v.png)';
                    }
                    else if (x2 - x1 == 3){
                        img = 'url(/static/web/style/res/ship4_' + (i - x1 + 1) + 'v.png)';
                    }
                    p1_original_values[block_id] = img;
                    $("#1_"+block_id+"").css('background-image', img);
                    $("#1_"+block_id+"").attr('class', 'ship');
                }
            }
            else{
                for (var i = x2; i <= x1; ++i){
                    var block_id = i * 10 + y1;
                    var img = 'none';
                    if (x1 - x2 == 1){
                        img = 'url(/static/web/style/res/ship2_' + (i - x2 + 1) + 'v.png)';
                    }
                    else if (x1 - x2 == 2){
                        img = 'url(/static/web/style/res/ship3_' + (i - x2 + 1) + 'v.png)';
                    }
                    else if (x1 - x2 == 3){
                        img = 'url(/static/web/style/res/ship4_' + (i - x2 + 1) + 'v.png)';
                    }
                    p1_original_values[block_id] = img;
                    $("#1_"+block_id+"").css('background-image', img);
                    $("#1_"+block_id+"").attr('class', 'ship');
                }
            }
        }
        else{
            if (y1 <= y2){
                for (var i = y1; i <= y2; ++i){
                    var block_id = x1 * 10 + i;
                    var img = 'none';
                    if (y2 - y1 == 1){
                        img = 'url(/static/web/style/res/ship2_' + (i - y1 + 1) + '.png)';
                    }
                    else if (y2 - y1 == 2){
                        img = 'url(/static/web/style/res/ship3_' + (i - y1 + 1) + '.png)';
                    }
                    else if (y2 - y1 == 3){
                        img = 'url(/static/web/style/res/ship4_' + (i - y1 + 1) + '.png)';
                    }
                    p1_original_values[block_id] = img;
                    $("#1_"+block_id+"").css('background-image', img);
                    $("#1_"+block_id+"").attr('class', 'ship');
                }
            }
            else{
                for (var i = y2; i <= y1; ++i){
                    var block_id = x1 * 10 + i;
                    var img = 'none';
                    if (y1 - y2 == 1){
                        img = 'url(/static/web/style/res/ship2_' + (i - y2 + 1) + '.png)';
                    }
                    else if (y1 - y2 == 2){
                        img = 'url(/static/web/style/res/ship3_' + (i - y2 + 1) + '.png)';
                    }
                    else if (y1 - y2 == 3){
                        img = 'url(/static/web/style/res/ship4_' + (i - y2 + 1) + '.png)';
                    }
                    p1_original_values[block_id] = img;
                    $("#1_"+block_id+"").css('background-image', img);
                    $("#1_"+block_id+"").attr('class', 'ship');
                }
            }
        }
    });

    var p2_ships = $('#player2').val() + "_ship";
    $("[name="+p2_ships+"]").each(function(index){
        var coordinates = [];
        $(this).children().each(function(iindex){
            coordinates.push($(this).html());
        });
        x1 = parseInt(coordinates[0]);
        y1 = parseInt(coordinates[1]);
        x2 = parseInt(coordinates[2]);
        y2 = parseInt(coordinates[3]);
        if (y1 == y2){
            if (x1 <= x2){
                for (var i = x1; i <= x2; ++i){
                    var block_id = i * 10 + y1;
                    var img = 'none';
                    if (x2 == x1){
                        img = 'url(/static/web/style/res/ship1_1.png)';
                    }
                    else if (x2 - x1 == 1){
                        img = 'url(/static/web/style/res/ship2_' + (i - x1 + 1) + 'v.png)';
                    }
                    else if (x2 - x1 == 2){
                        img = 'url(/static/web/style/res/ship3_' + (i - x1 + 1) + 'v.png)';
                    }
                    else if (x2 - x1 == 3){
                        img = 'url(/static/web/style/res/ship4_' + (i - x1 + 1) + 'v.png)';
                    }
                    p2_original_values[block_id] = img;
                    $("#2_"+block_id+"").css('background-image', img);
                    $("#2_"+block_id+"").attr('class', 'ship');
                }
            }
            else{
                for (var i = x2; i <= x1; ++i){
                    var block_id = i * 10 + y1;
                    var img = 'none';
                    if (x1 - x2 == 1){
                        img = 'url(/static/web/style/res/ship2_' + (i - x2 + 1) + 'v.png)';
                    }
                    else if (x1 - x2 == 2){
                        img = 'url(/static/web/style/res/ship3_' + (i - x2 + 1) + 'v.png)';
                    }
                    else if (x1 - x2 == 3){
                        img = 'url(/static/web/style/res/ship4_' + (i - x2 + 1) + 'v.png)';
                    }
                    p2_original_values[block_id] = img;
                    $("#2_"+block_id+"").css('background-image', img);
                    $("#2_"+block_id+"").attr('class', 'ship');
                }
            }
        }
        else{
            if (y1 <= y2){
                for (var i = y1; i <= y2; ++i){
                    var block_id = x1 * 10 + i;
                    var img = 'none';
                    if (y2 - y1 == 1){
                        img = 'url(/static/web/style/res/ship2_' + (i - y1 + 1) + '.png)';
                    }
                    else if (y2 - y1 == 2){
                        img = 'url(/static/web/style/res/ship3_' + (i - y1 + 1) + '.png)';
                    }
                    else if (y2 - y1 == 3){
                        img = 'url(/static/web/style/res/ship4_' + (i - y1 + 1) + '.png)';
                    }
                    p2_original_values[block_id] = img;
                    $("#2_"+block_id+"").css('background-image', img);
                    $("#2_"+block_id+"").attr('class', 'ship');
                }
            }
            else{
                for (var i = y2; i <= y1; ++i){
                    var block_id = x1 * 10 + i;
                    var img = 'none';
                    if (y1 - y2 == 1){
                        img = 'url(/static/web/style/res/ship2_' + (i - y2 + 1) + '.png)';
                    }
                    else if (y1 - y2 == 2){
                        img = 'url(/static/web/style/res/ship3_' + (i - y2 + 1) + '.png)';
                    }
                    else if (y1 - y2 == 3){
                        img = 'url(/static/web/style/res/ship4_' + (i - y2 + 1) + '.png)';
                    }
                    p2_original_values[block_id] = img;
                    $("#2_"+block_id+"").css('background-image', img);
                    $("#2_"+block_id+"").attr('class', 'ship');
                }
            }
        }
    });
});

var p1_index = 0;
var p2_index = 0;
var p1_hit = 0;
var p2_hit = 0;
var p1_shots = []
var p2_shots = []
function next(){
    var shot = false;
    if (p1_index == p2_index){
        $('#current_shooter').html("It's " + $('#player2').val() + "'s turn to shoot.");
        var p1_shot = $('#player1').val() + "_shot";
        $("[name="+p1_shot+"]").each(function(index){
            if (index == p1_index){
                var coordinates = [];
                $(this).children().each(function(iindex){
                    coordinates.push($(this).html());
                });
                x = parseInt(coordinates[0]);
                y = parseInt(coordinates[1]);
                var block_id = x * 10 + y;
                var new_image = 'none'
                if ($("#2_"+block_id+"").attr('class') == 'ship'){
                    p1_hit = p1_hit + 1;
                    new_image = 'url(/static/web/style/res/hit.jpg)';
                }
                else
                    new_image = 'url(/static/web/style/res/miss.jpg)';

                $("#2_"+block_id+"").animate({'opacity': 0.5}, 300, function() {
                    $(this).css('background-image', new_image);
                    $(this).animate({'opacity': 1}, 300);
                })
                shot = true;
                p1_shots.push(block_id);
            }
        });
        p1_index = p1_index + 1;
    }
    else{
        $('#current_shooter').html("It's " + $('#player1').val() + "'s turn to shoot.");
        var p2_shot = $('#player2').val() + "_shot";
        $("[name="+p2_shot+"]").each(function(index){
            if (index == p2_index){
                var coordinates = [];
                $(this).children().each(function(iindex){
                    coordinates.push($(this).html());
                });
                x = parseInt(coordinates[0]);
                y = parseInt(coordinates[1]);
                var block_id = x * 10 + y;
                var new_image = 'none';
                if ($("#1_"+block_id+"").attr('class') == 'ship'){
                    p2_hit = p2_hit + 1;
                    new_image = 'url(/static/web/style/res/hit.jpg)';
                }
                else
                    new_image = 'url(/static/web/style/res/miss.jpg)';

                $("#1_"+block_id+"").animate({'opacity': 0.5}, 300, function() {
                    $(this).css('background-image', new_image);
                    $(this).animate({'opacity': 1}, 300);
                })
                shot = true;
                p2_shots.push(block_id);
            }
        });
        p2_index = p2_index + 1;
    }

    if (p1_hit == 20){
        setTimeout(function() { alert($('#player1').val() + " has won the game!"); }, 600);
        $("#nextButton").prop("disabled", true);
    }
    if (p2_hit == 20){
        setTimeout(function() { alert($('#player2').val() + " has won the game!"); }, 600);
        $("#nextButton").prop("disabled", true);
    }

    $('#prevButton').prop("disabled", false);

    if (p2_hit < 20 && p1_hit < 20 && shot == false){
        var winner = $('#winner').val();
        var loser;
        if (winner == $('#player1').val())
            loser = $('#player2').val();
        else
            loser = $('#player1').val();
        setTimeout(function() { alert(loser + " has left the game. " + winner + " was declared as a winner!"); }, 600);
        $("#nextButton").prop("disabled", true);
    }
}

function prev(){
    if (p1_index != p2_index){
        $('#current_shooter').html("It's " + $('#player1').val() + "'s turn to shoot.");
        var block_id = p1_shots.pop();
        $("#2_"+block_id+"").css('background-image', p2_original_values[block_id]);
        if ($("#2_"+block_id+"").attr('class') == 'ship'){
            p1_hit = p1_hit - 1;
        }

        p1_index -= 1;
    }
    else{
        $('#current_shooter').html("It's " + $('#player2').val() + "'s turn to shoot.");
        var block_id = p2_shots.pop();
        $("#1_"+block_id+"").css('background-image', p1_original_values[block_id]);
        if ($("#1_"+block_id+"").attr('class') == 'ship'){
            p2_hit = p2_hit - 1;
        }

        p2_index -= 1;
    }

    $('#nextButton').prop("disabled", false);
    if (p1_index == 0 && p2_index == 0){
        $("#prevButton").prop("disabled", true);
    }
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

function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

var isStopCommand = false;

function autoplay(){
    isStopCommand = false;
    playLoop();
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