import importlib.util
import glob
import os
import sys
import __main__
import filecmp
import shutil

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

python = sys.executable
extentions_folder = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)),
                                 "web" + os.sep + "extensions" + os.sep + "dzNodes")
javascript_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")
outdate_file_list = ['comfy_shared.js', 'debug.js', 'mtb_widgets.js', 'parse-css.js', 'dz_widgets.js']

if not os.path.exists(extentions_folder):
    print('# 😺dzNodes: Making the "web\extensions\dzNodes" folder')
    os.mkdir(extentions_folder)
else:
    for i in outdate_file_list:
        outdate_file = os.path.join(extentions_folder, i)
        if os.path.exists(outdate_file):
            os.remove(outdate_file)

result = filecmp.dircmp(javascript_folder, extentions_folder)

if result.left_only or result.diff_files:
    print('# 😺dzNodes: Update to javascripts files detected')
    file_list = list(result.left_only)
    file_list.extend(x for x in result.diff_files if x not in file_list)

    for file in file_list:
        print(f'# 😺dzNodes:: Copying {file} to extensions folder')
        src_file = os.path.join(javascript_folder, file)
        dst_file = os.path.join(extentions_folder, file)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_file)


def get_ext_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(__file__)
    if subpath is not None:
        dir = os.path.join(dir, subpath)

    dir = os.path.abspath(dir)

    if mkdir and not os.path.exists(dir):
        os.makedirs(dir)
    return dir

py = get_ext_dir("py")
files = os.listdir(py)
nodes_tristan_needs = [
        # We just need these 3 nodes
        "hl_frequency_detail_restore.py",  # LayerUtility: H/L Frequency Detail Restore
        "color_correct_auto_adjust_v2.py", # LayerColor: AutoAdjust V2
        "color_correct_levels.py",         # LayerColor: Levels
]
for file in files:
    if not file.endswith(".py"):
        continue
    if file not in nodes_tristan_needs:
        continue
    name = os.path.splitext(file)[0]
    imported_module = importlib.import_module(".py.{}".format(name), __name__)
    try:
        # To be able to install and use alongside the upstream package, give a unique prefix, and give the display names a unique suffix and emoji
        NODE_CLASS_MAPPINGS = { 
            **NODE_CLASS_MAPPINGS,
            **{f"Rdancer_{key}": value for key, value in imported_module.NODE_CLASS_MAPPINGS.items()}
        }   
        NODE_DISPLAY_NAME_MAPPINGS = { 
            **NODE_DISPLAY_NAME_MAPPINGS,
            **{f"Rdancer_{key}": f"{value} (Lite 💃)" for key, value in imported_module.NODE_DISPLAY_NAME_MAPPINGS.items()}
        }   
    except:
        pass

# Print NODE_CLASS_MAPPINGS for debugging
print("Updated NODE_CLASS_MAPPINGS:")
for key, value in NODE_CLASS_MAPPINGS.items():
    print(f"{key}: {value}")
# Print NODE_DISPLAY_NAME_MAPPINGS for debugging
print("\nUpdated NODE_DISPLAY_NAME_MAPPINGS:")
for key, value in NODE_DISPLAY_NAME_MAPPINGS.items():
    print(f"{key}: {value}")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
