var FlashService = {};
FlashService.defaultTime = 5000;

FlashService.success = function (className, message, time) {
    if (typeof className == 'undefined') {
        throw "Class name to apply the service is mandatory";
    }
    if (typeof message == 'undefined') {
        throw "Message content must not be null";
    }
    className = '#' + className;
    time = time || FlashService.defaultTime;
    $(className)[0].innerHTML = "<div class='flash-success flash-message'>" + '&#10004  ' + message + "</div>";
    setTimeout(function () {
        $(className)[0].innerHTML = "";
    }, time);
};

FlashService.error = function (className, message, time) {
    if (typeof className == 'undefined') {
        throw "Class name to apply the service is mandatory";
    }
    if (typeof message == 'undefined') {
        throw "Message content must not be null";
    }
    className = '#' + className;
    time = time || FlashService.defaultTime;
    $(className)[0].innerHTML = "<div class='flash-error flash-message'>" + '&#10008  ' + message + "</div>";

    setTimeout(function () {
        $(className)[0].innerHTML = "";
    }, time);
};

FlashService.clear = function (className) {
    $('#flash-container')[0].innerHTML = "";
};