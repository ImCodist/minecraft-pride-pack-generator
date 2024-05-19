avaliableFlags = {}


// MISC FUNCTIONS
function updateFlagSelects() {
    $.ajax("flags", {success: function(result) {
        avaliableFlags = result;
        setupModules();
    }});
}

function doToggleSegment(checkboxId, segmentId) {
    is_enabled = $(`#${checkboxId}`).prop("checked");

    segment = $(`#${segmentId}`);
    if (is_enabled == false) {
        segment.hide();
    } else {
        segment.show();
    }
}


function fillDropdownWithFlags(dropdownId) {
    $(`#${dropdownId}`).empty();

    Object.keys(avaliableFlags).forEach(flagID => {
        flagData = avaliableFlags[flagID];

        html = `<div class="item" data-value="${flagID}"><img src="/assets/preview/${flagID}">${flagData.name}</div>`;

        $(`#${dropdownId}`).append(html);
    });
}


function updateUIStuffs() {
    $('.ui.checkbox').checkbox();
    $('.selection.dropdown').dropdown();
}


function warn(message) {
    alert(message);
}


// EXPERIENCE BAR MODULE
function setupExperienceBar() {
    // setup flag ids
    fillDropdownWithFlags("_xp_bar_flag_menu")
    fillDropdownWithFlags("_xp_bar_flag_bg_menu")

    $("#xp_bar_do_bg").on("change", () => {updateExperienceBar()})
    $("#xp_bar_unique_bg").on("change", () => {updateExperienceBar()})

    updateExperienceBar();
}

function updateExperienceBar() {
    use_bg = $("#xp_bar_do_bg").prop("checked");
    if (use_bg == false) {
        $("#xp_bar_unique_bg").parent().addClass("disabled");
    } else {
        $("#xp_bar_unique_bg").parent().removeClass("disabled");
    }

    use_unique_bg = $("#xp_bar_unique_bg").prop("checked");
    unique_bg_root = $("#xp_bar_flag_bg").parent().parent().parent();
    if (use_unique_bg == false || use_bg == false) {
        unique_bg_root.hide();
    } else {
        unique_bg_root.show();
    }
}


// HEARTS MODULE
function setupHearts() {
    fillDropdownWithFlags("_hearts_flag_menu")
}


// ENCHANTED GLINT
function setupEnchantedGlint() {
    fillDropdownWithFlags("_e_glint_flag_menu")
}


// SETUP FOR MODULES
function setupModules() {
    setupExperienceBar();
    setupHearts();
    setupEnchantedGlint();

    updateUIStuffs();
}

function updateModules() {
    updateExperienceBar();
}


// GENERATE THE PACK
function generate() {
    msg_flag_not_null = "flag should not be empty"

    data = {}
    
    xp_bar_enabled = $("#xp_bar_enabled").prop("checked");
    if (xp_bar_enabled) {
        data["xp_bar_flag_id"] = $("#xp_bar_flag").val();
        data["xp_bar_do_bg"] = $("#xp_bar_do_bg").prop("checked");

        if (data["xp_bar_flag_id"] == "") {
            warn(msg_flag_not_null)
            return;
        }

        unique_bg_flag = $("#xp_bar_unique_bg").prop("checked");
        if (unique_bg_flag) {
            data["xp_bar_flag_bg_id"] = $("#xp_bar_flag_bg").val();

            if (data["xp_bar_flag_bg_id"] == "") {
                warn(msg_flag_not_null)
                return;
            }
        }
    }

    hearts_enabled = $("#hearts_enabled").prop("checked");
    if (hearts_enabled) {
        data["hearts_flag_id"] = $("#hearts_flag").val();

        if (data["hearts_flag_id"] == "") {
            warn(msg_flag_not_null)
            return;
        }
    }

    e_glint_enabled = $("#e_glint_enabled").prop("checked");
    if (e_glint_enabled) {
        data["e_glint_flag_id"] = $("#e_glint_flag").val();

        if (data["e_glint_flag_id"] == "") {
            warn(msg_flag_not_null)
            return;
        }
    }

    if (Object.keys(data).length == 0) {
        warn("im not generating an empty pack silly")
        return;
    }
    
    window.location.href = `generate?${$.param(data)}`;
}


// ON READY
$(function () {
    updateUIStuffs();

    setupModules();
    updateModules();

    updateFlagSelects();

    $("#generate").on("click", () => {
        generate();
    })
});