import flags
import generate
import io
import os
from flask import Flask, render_template, send_file, request


FLAG_DIRECTORY = "assets/flags"

FILE_DOWNLOAD_NAME = "pride pack.zip"

ASSET_MISSING_FLAG_PREVIEW = "assets/images/flag_missing.png"


flag_data = flags.get_data_from_dir(FLAG_DIRECTORY)

previews = {}
for flag in flag_data:
    cur_flag_data = flag_data[flag]
    
    data = {}
    
    data["flag"] = generate.generate_flag_preview(cur_flag_data)
    
    previews[flag] = data


# Web app
app = Flask(__name__)


@app.route("/")
def route_index():
    return render_template("index.html")

@app.route('/flags')
def route_flags():
    flag_ids = {}
    for flag in flag_data:
        this_flag_data = flag_data[flag]
        flag_ids[flag] = {
            "name": this_flag_data.name
        }
    
    return flag_ids

@app.route("/assets/preview/<flag_id>")
def route_assets_flag(flag_id):
    preview_image = previews.get(flag_id, {}).get("flag", None)
    
    if preview_image:
        image_io = io.BytesIO()
        preview_image.save(image_io, "PNG")
        image_io.seek(0)
        
        return send_file(image_io, mimetype="image/png")

    return send_file(ASSET_MISSING_FLAG_PREVIEW)

@app.route('/generate')
def route_generate():
    # Get possible arguments.
    xp_bar_flag_id = request.args.get("xp_bar_flag_id", "")
    xp_bar_do_bg = (request.args.get("xp_bar_do_bg", "") == "true")
    xp_bar_bg_flag_id = request.args.get("xp_bar_flag_bg_id", "")
    
    hearts_flag_id = request.args.get("hearts_flag_id", "")
    
    enchanted_glint_flag_id = request.args.get("e_glint_flag_id", "")
    
    # Get data from arguments.
    xp_bar_flag_data = flag_data.get(xp_bar_flag_id, None)
    
    xp_bar_bg_flag_data = None
    if xp_bar_do_bg:
        xp_bar_bg_flag_data = flag_data.get(xp_bar_bg_flag_id, None)
        if not xp_bar_bg_flag_data:
            xp_bar_bg_flag_data = xp_bar_flag_data

    hearts_flag_data = flag_data.get(hearts_flag_id, None)
    
    enchanted_glint_flag_data = flag_data.get(enchanted_glint_flag_id, None)
    
    # Create the package.
    package_data = generate.generate_package(
        xp_bar_flag=xp_bar_flag_data,
        xp_bar_bg_flag=xp_bar_bg_flag_data,
        
        hearts_flag=hearts_flag_data,
        
        enchanted_glint_flag=enchanted_glint_flag_data
    )
    
    if package_data:
        output_path = package_data.package()
        
        # convert the file to bytes
        output_file = open(output_path, "rb")
        
        file_bytes = io.BytesIO()
        file_bytes.write(output_file.read())
        file_bytes.seek(0)
        
        output_file.close()
        
        # then kill the file
        os.remove(output_path)

        return send_file(
            file_bytes,
            download_name=FILE_DOWNLOAD_NAME
        )

    return "Could not generate package."