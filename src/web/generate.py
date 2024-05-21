"""
Returns a generated resource pack based on user provided arguments.
Has no visual front end.
"""


from flask import Blueprint, request, send_file
from components import experience_bar, hearts, enchanted_glint
from data.package import PackageData, PACK_FILE_NAME


def parse_request_args(args) -> dict:
    parsed_args = {}
    
    # go through all the args and convert them from A[B] into parent A and child B in a dict
    # this doesnt go a level deeper and do children of the children but i dont need it to do that
    for arg in args:
        value = args[arg]
        
        split = arg.split("[")
        
        # ignore anything that doesnt have a child
        if len(split) <= 1:
            parsed_args[arg] = value
            continue
        
        arg_main = split[0]
        
        arg_child = split[1]
        arg_child = arg_child[0:len(arg_child)-1]
        
        # add the dict of the parent if it does not exist yet
        if not arg_main in parsed_args.keys():
            parsed_args[arg_main] = {}
        
        parsed_args[arg_main][arg_child] = value
    
    return parsed_args


def get_base_component_from_id(id: str):
    base_component = None
    
    match id:
        case "xp_bar":
            base_component = experience_bar.ComponentExperienceBar()
        case "hearts":
            base_component = hearts.ComponentHearts()
        case "e_glint":
            base_component = enchanted_glint.ComponentEnchantedGlint()
    
    return base_component


bp = Blueprint("generate", __name__)


@bp.route("/generate")
def generate():
    parsed_args = parse_request_args(request.args)
    
    components = []
    
    # loop through every possible component and add it to the components list if it exists
    for component_id in parsed_args.keys():
        new_component = get_base_component_from_id(component_id)
        
        # add the given options to the component and add it to the components list
        if new_component:
            new_component.options = parsed_args[component_id]
            components.append(new_component)
    
    # dont generate empty resource packs
    if len(components) == 0:
        return "nice try but im not generating an empty resource pack<br>why do you want this"
    
    # create the package and send it to the user
    package = PackageData(components)
    
    final_result = package.package()
    final_result.seek(0)
    
    return send_file(final_result, download_name=PACK_FILE_NAME, as_attachment=True)