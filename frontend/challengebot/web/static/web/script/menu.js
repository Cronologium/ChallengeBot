$(document).ready(function () {
    var keyboard_clicked = false;
    $('#mixer').css('cursor', 'pointer');
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
        if (keyboard_clicked == true)
            return;
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

    $('#mixer').click(function() {
        var doc = document.documentElement;
        var top = Math.round((window.pageYOffset || doc.scrollTop)  - (doc.clientTop || 0));
        var menu_size = $("#menu").css("height");
        menu_size = parseInt(menu_size.substring(0, menu_size.length - 2));
        var ratio = (menu_size - top) / menu_size;
        if (keyboard_clicked == false)
        {
            if (ratio > 0.4)
            {
                return;
            }
            $('#menu').css('position', 'fixed');
            $('#mixer').css("transform", "scale(" + String(1.0) + "," + String(1.0) + ")");

            var top_position = menu_size;
            $("#mixer").css("top", String(top_position) + "px");
            var padding_top_size = menu_size + 100;
            var content_margin = String(padding_top_size) + "px";
            $('#content-wrapper').css("padding-top", content_margin);
            keyboard_clicked = true;
        }
        else
        {
            if (ratio > 0.4)
            {
                return;
            }
            $('#menu').css('position', '');
            $('#content-wrapper').css("padding-top", '100px');
            keyboard_clicked = false;
            change_size();
        }
    });



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