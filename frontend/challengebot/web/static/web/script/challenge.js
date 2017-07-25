function validate_opponents(){
    var selected_opponents = document.getElementById("id_selected_opponents");
    var options = selected_opponents && selected_opponents.options;
    for (var i = 0; i<options.length; i++){
        options[i].selected = true;
    }
}

function remove_opponent(){
    var selected_opponents = document.getElementById("id_selected_opponents");
    var all_selected = [];
    var options = selected_opponents && selected_opponents.options;
    var opt;

    for (var i = 0; i<options.length; i++){
        opt = options[i];
        if (opt.selected){
            selected_opponents.remove(i);
            i = 0;
        }
    }
}

function add_opponent(){
    var selected_opponents = document.getElementById("id_selected_opponents");
    var current_opponents = document.getElementById("id_eligible_opponents");
    var options = selected_opponents && selected_opponents.options;

    var min_players = document.getElementById("min_players");
    var max_players = document.getElementById("max_players");
    for (var k = 0; k < current_opponents.length; ++k) {
        if (!current_opponents[k].selected)
            continue;
        if (options.length + 1 >= max_players.value){
            alert("Max opponents reached!");
            return;
        }
        var ok = true;
        for (var i = 0; i < options.length; ++i){
            var opt = options[i];
            if (opt.value == current_opponents.options[k].value){
                ok = false;
            }
        }
        if (ok) {
            var option = document.createElement('option');
            option.value = current_opponents.options[k].value;
            option.text = current_opponents.options[k].text;
            selected_opponents.appendChild(option);
        }
    }
}