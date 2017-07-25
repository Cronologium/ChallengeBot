$( document ).ready(function() {

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

     $( window ).resize(change_opacity);

     function change_opacity() {
        var s = $(window).width() * 1.0;
        var minw_css = $("body").css("min-width");
        var min_w = parseInt(minw_css.substring(0, minw_css.length - 2));
        var op = 1.0;
        if (s < min_w)
            op = 0.2;
        else
            if (s < min_w + 400)
                op = 0.2 + (s - min_w) / 400 * 0.8;
        $("#mixer").css("opacity", String(op));
     }

     $("#user-button").mouseenter(function () {
        $(".user-face").attr("id", "user-face-showing");
     });

     $("#user-button").mouseleave( function () {
        $(".user-face").attr("id", "");
     })

     $("#logout-button").mouseenter(function () {
        $(".user-face").attr("id", "user-face-hiding");
     });

     $("#logout-button").mouseleave( function () {
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

     change_opacity();
});