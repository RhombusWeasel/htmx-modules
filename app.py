import requests
import json
import os
from flask import Flask, render_template, request, Blueprint

requests.packages.urllib3.disable_warnings()

# Register blueprints will walk the file system and register all blueprints in the blueprints folder
# This is a simple way to add new blueprints without having to modify this file in fact from here we 
# can expose an API to the other blueprints to use.
# Each blueprint may have a url_prefix attribute that will be used to register the blueprint
# If the url_prefix is not specified then the blueprint name will be used as the url_prefix
# For example the blueprint name "api" will be registered with a url_prefix of "/api" if not specified.
# Each blueprint MUST contain a Blueprint object within it's namespace, this will be used to register 
# the blueprint
def register_blueprints(app: Flask) -> None:
    # Iterate the blueprints folder and register each blueprint
    for root, dirs, files in os.walk('blueprints'):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                blueprint = os.path.join(root, file).split(
                    os.sep, 1)[1].replace(os.sep, '.')[:-3]
                print(f'Registering blueprint: {blueprint}')
                bp = __import__(f'blueprints.{blueprint}', fromlist=[blueprint])
                page = getattr(bp, 'url_prefix', '/' + blueprint.split('.')[-1])
                for obj in vars(bp).values():
                    if isinstance(obj, Blueprint):
                        app.register_blueprint(
                            obj, url_prefix=page)

app = Flask(__name__)
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)