from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

url_prefix = '/'

routes = Blueprint('simple_page', __name__,
                   template_folder='templates')


@routes.route('/', defaults={'page': 'index'})
@routes.route('/<page>')
def show(page):
    try:
        return render_template(f'{page}.html')
    except TemplateNotFound:
        abort(404)
