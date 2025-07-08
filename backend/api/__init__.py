from flask import Blueprint
try:
    from .companies import companies_api
except ImportError:
    from backend.api.companies import companies_api

api_bp = Blueprint("api",__name__)
api_bp.register_blueprint(companies_api,url_prefix="/companies")
