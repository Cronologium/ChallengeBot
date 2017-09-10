(function ($) {
    var defaultTime = 5000;
    Flash = {};
    Flash.success = function (msg, time) {
        time = time || defaultTime;
        $('#flash-container')[0].innerHTML = "<div class='flash-success flash-message'>" + '&#10004  ' + msg + "</div>";
        setTimeout(function () {
            $('#flash-container')[0].innerHTML = "";
        }, time);
    };

    Flash.error = function (msg, time) {
        time = time || defaultTime;
        $('#flash-container')[0].innerHTML = "<div class='flash-error flash-message'>" + '&#10008  ' + msg + "</div>";

        setTimeout(function () {
            $('#flash-container')[0].innerHTML = "";
        }, time);
    };

    Flash.clear = function () {
        $('#flash-container')[0].innerHTML = "";
    };

})(jQuery);

$(function () {
    Flash.clear();

});