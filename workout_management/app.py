import importlib
import inspect
import pkgutil

from flask import Flask, Blueprint

from workout_management.config import ENVIRONMENTS, ConfigEnum
from workout_management.extensions import db_context, alembic
from workout_management.middleware import add_content_type_header
from workout_management.resources.ping import ping_blueprint


def __get_blueprint_from_resource_module():
    modules = importlib.import_module("workout_management.resources")
    packages = [item for item in pkgutil.walk_packages(modules.__path__) if item.ispkg is True]

    blueprints = list()

    for _loader, name, is_pkg in packages:
        resource_route_module = importlib.import_module(f"workout_management.resources.{name}.routes")
        members = inspect.getmembers(resource_route_module)

        module_blueprints = [item[1] for item in members if isinstance(item[1], Blueprint)]

        blueprints += module_blueprints

    return blueprints


def register_blueprints(app):
    blueprints = __get_blueprint_from_resource_module()

    for bp in blueprints:
        app.register_blueprint(bp)

    app.register_blueprint(ping_blueprint)


def register_extensions(app):
    db_context.init_app(app)
    alembic.init_app(app, True, "db")
    return None


def register_middlewares(app):
    app.after_request(add_content_type_header)
    return None


def create_app(env=ConfigEnum.Development):
    app = Flask(__name__)
    app.config.from_object(ENVIRONMENTS[env])
    register_extensions(app)
    register_blueprints(app)
    register_middlewares(app)

    with app.app_context():
        alembic.upgrade()

    return app


if __name__ == '__main__':
    create_app().run()
