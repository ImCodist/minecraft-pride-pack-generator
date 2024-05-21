$(function() {
    // update any classes that need to display the version number
    $.get("data/version", {}, function(result) {
        versionInfo = result.version

        gitSha = result.git_sha_short
        if (gitSha != "") {
            versionInfo += "+" + gitSha
        }

        $(".get_version").html("v" + versionInfo)
    })
})