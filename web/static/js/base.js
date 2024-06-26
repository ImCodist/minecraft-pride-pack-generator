$(function() {
    // update any classes that need to display the version number
    $.get("data/version", {}, function(result) {
        versionInfo = result.full
        $(".get_version").html("v" + versionInfo)
    })

    // set the header icon to a random flag!
    $("#pack_png_random").hide()
    $("#pack_png_random_placeholder").show()

    $.get("data/flags", {}, function(result) {
        flag_ids = Object.keys(result)
        random_flag = flag_ids[Math.floor(Math.random() * flag_ids.length)]

        $("#pack_png_random").attr("src", `/assets/packpng?flag=${random_flag}`);
        $("#pack_png_random").one("load", function(){
            $("#pack_png_random").show()
            $("#pack_png_random_placeholder").hide()
        })
    })

    // set the navbars avtive
    $("#navbar").children().each(function(navitem) {
        if ($(this).attr("href") == window.location.pathname) {
            $(this).addClass("active")
        }
    })

    // nag the user if they are on mobile
    if (navigator.userAgent.match(/Mobile/)) {
        $("#mobile_nag").nag()
    }
})