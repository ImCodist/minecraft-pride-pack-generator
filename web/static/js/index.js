// all javascript code is REALLY low effort
// i hate javascript
// i hate javascript
// i. hate. javascript.
// but i love you :)


dataTable = {}


$(function() {
    // register all components on the page
    registerComponents()

    // setup flag dropdowns
    registerFlagDropdowns()
    
    // setup main controls (download button, etc..)
    registerMainControls()
})


// COMPONENT STUFF

function registerComponents() {
    $(".component_segment").each(function() {
        component = $(this)

        // get the neccessary variables for registering a component
        componentHeader = component.children(".component_header").first()
        componentCheckbox = componentHeader.children(".component_checkbox").first()

        // hide the options depending on checkbox state.
        componentCheckbox.checkbox({
            onChange: function() {
                component = $(this).parent().parent().parent()
                updateComponent(component)
            }
        })

        updateComponent(component);
    })
}

function updateComponent(component) {
    componentHeader = component.children(".component_header").first()
    componentCheckbox = componentHeader.children(".component_checkbox").first()

    componentContent = component.children(".component_content")

    // hide the options if the checkbox is not checked
    isChecked = componentCheckbox.checkbox("is checked")

    if (isChecked) componentContent.show()
    else componentContent.hide()
}


// CUSTOM HTML THINGYS

function registerFlagDropdowns() {
    // add a loading animation
    $(".flag_select").addClass("loading")
    $(".flag_select").addClass("read-only")

    // get flag data from the server
    $.get("data/flags", {}, function(result) {
        flags = result

        // move flag data into the dropdown
        values = []
        for (const flagId in flags) {
            flagData = flags[flagId]

            html = `<div class="item" data-value="${flagId}"><img src="assets/flags?flag=${flagId}">${flagData.name}</div>`;
            $(".flag_select").children(".menu").append(html);
        }

        // setup dropdown
        $(".flag_select").dropdown()
        $(".flag_select").children(".text.default").html("Select Flag")

        // clear loading animation
        $(".flag_select").removeClass("loading")
        $(".flag_select").removeClass("read-only")
    })
}

function registerMainControls() {
    $("#download_button").on("click", function() {
        download()
    })
}


// ACTUAL LIKE FUNCTIONAL STUFF

function download() {
    hasError = null

    dataValues = {}
    
    // get all the values and put only the used ones in an object
    for (const component in dataTable) {
        componentDataValues = {}
        componentDataTable = dataTable[component]

        // only get values for enabled components
        isEnabled = $(`#c_${component}_checkbox`).checkbox("is checked")
        if (!isEnabled) continue

        for (const dataValue in componentDataTable) {
            dataValueId = componentDataTable[dataValue]

            dataValueIdObject = $(`#${dataValueId}`)
            dataValueIdObjectValue = null

            // set the value of this object based on what type it is
            if (dataValueIdObject.hasClass("dropdown")) {
                dataValueIdObjectValue = dataValueIdObject.dropdown("get value")
            }
            if (dataValueIdObject.hasClass("checkbox")) {
                dataValueIdObjectValue = dataValueIdObject.checkbox("is checked")
            }

            componentDataValues[dataValue] = dataValueIdObjectValue
        }

        dataValues[component] = componentDataValues
    }

    // check for errors
    if (Object.keys(dataValues).length == 0) {
        hasError = `you cant generate an empty pack silly!!!!`
    } else {
        flagRequiredMsg = "flag value is required"
        requiresFlags = ["xp_bar", "hearts", "e_glint"]

        missingFlags = []
        
        for (const component of requiresFlags) {
            if (Object.keys(dataValues).includes(component)) {
                if (dataValues[component]["flag"] == "") missingFlags.push(component)
                
                // special case for the xp bar as it can have two unique flags
                if (component == "xp_bar") {
                    if (
                        dataValues[component]["unique_bg"] == true && 
                        dataValues[component]["bg_flag"] == ""
                    ) missingFlags.push(component + " (bg flag)")
                }
            }
        }

        if (missingFlags.length > 0) {
            hasError = flagRequiredMsg + ` [${missingFlags.join(", ")}]`
        }
    }

    if (hasError) {
        $.toast({
            class: "error",
            title: `could not generate pack`,
            message: hasError
        });

        return
    }
    
    // create the generate url
    baseURL = "generate"
    finalURL = baseURL + "?" + $.param(dataValues);

    // take the user to the generate endpoint with arguments
    window.location.href = `${finalURL}`;
}