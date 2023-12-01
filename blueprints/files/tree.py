# A simple flask blueprint showing a backend API implementation
from flask import Blueprint, render_template, jsonify
import os

api = Blueprint('api', __name__, url_prefix='/api', template_folder='templates')

show_hidden = False
path = '.'
paths = []
folders = []
open_paths = []

def tree(path):
    global paths, folders
    for file in os.listdir(path):
        if(file.startswith('.') or file.startswith('_')) and show_hidden == False:
            continue
        full_path = os.path.join(path, file)
        if os.path.isdir(full_path):
            if not full_path in folders:
                folders.append(full_path)
        else:
            if not full_path in paths:
                paths.append(full_path)
    paths = sorted(paths, key=lambda x: x.lower())

tree('.')

@api.route('/list_files')
def list_files():
    return render_template('tree_viewer.html', files=paths, folders=folders, open_paths=open_paths, cur_path='.')

@api.route('toggle_folder/<path:path>', methods=['GET'])
def toggle_folder(path):
    global open_paths
    path = f'./{path}'
    if path in open_paths:
        open_paths.remove(path)
        print(f'Closing {path}')
        # iterate backwards to remove all subfolders
        for f in reversed(paths):
            if f.startswith(path):
                print(f'Removing files {f}')
                paths.remove(f)
        # iterate backwards to remove all subfolders
        for f in reversed(folders):
            if f.startswith(path) and f != path:
                print(f'Removing folders {f}')
                folders.remove(f)
    else:
        open_paths.append(path)
        tree(path)
    print(open_paths, paths, folders)
    return render_template('tree_viewer.html', files=paths, folders=folders, open_paths=open_paths, cur_path='.')