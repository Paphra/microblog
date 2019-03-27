from flask import render_template
from app.errors import bp
from app import db
from flask_babel import _


@bp.app_errorhandler(404)
def not_found_error(error):
    render_template('errors/404.html', title=_("Error")), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html', title=_("Error")), 500
