$(document).ready(function () {

    $("#login-prompt").click(function () {
        $("#login-page").css("width", "100%");
        $("#menu").addClass("blurred");
        $("#content-wrapper").addClass("blurred");
    });

    $("#close-login-prompt").click(function () {
        $("#login-page").css("width", "0%");
        $("#menu").removeClass("blurred");
        $("#content-wrapper").removeClass("blurred");
    });

    $("#register-prompt").click(function () {
        $("#register-page").css("width", "100%");
        $("#menu").addClass("blurred");
        $("#content-wrapper").addClass("blurred");
    });

    $("#close-register-prompt").click(function () {
        $("#register-page").css("width", "0%");
        $("#menu").removeClass("blurred");
        $("#content-wrapper").removeClass("blurred");
    });

    $(window).on('scroll', change_size);

    function change_size() {
        var doc = document.documentElement;
        var top = Math.round((window.pageYOffset || doc.scrollTop)  - (doc.clientTop || 0));
        var menu_size = $("#menu").css("height");
        var min_ratio = 0.4;
        menu_size = parseInt(menu_size.substring(0, menu_size.length - 2));
        var max_top_position = -(min_ratio * 100);
        var ratio = (menu_size - top) / menu_size;

        if (ratio < min_ratio) {
            ratio = min_ratio;
        }

        var top_position = menu_size - top - (1 - ratio)*50;


        // console.log(top_position);
        // console.log(max_top_position);
        // console.log();

        if (top_position < max_top_position)
            top_position = max_top_position;

        $("#mixer").css("transform", "scale(" + String(ratio) + "," + String(ratio) + ")");
        $("#mixer").css("top", String(top_position) + "px");
    }

    function show_menu() {
        console.log("CALLED");
    }

    function hide_menu() {

    }

    $("#user-button").mouseenter(function () {
        $(".user-face").attr("id", "user-face-showing");
    });

    $("#user-button").mouseleave(function () {
        $(".user-face").attr("id", "");
    })

    $("#logout-button").mouseenter(function () {
        $(".user-face").attr("id", "user-face-hiding");
    });

    $("#logout-button").mouseleave(function () {
        $(".user-face").attr("id", "");
    })

    $("#login-prompt").mouseenter(function () {
        $(".user-face").attr("id", "");
    });

    $("#login-prompt").mouseleave(function () {
        $(".user-face").attr("id", "user-face-hiding");
    });

    $("#register-prompt").mouseenter(function () {
        $(".user-face").attr("id", "");
    });

    $("#register-prompt").mouseleave(function () {
        $(".user-face").attr("id", "user-face-hiding");
    });

    change_size();
});