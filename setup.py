from setuptools import setup

setup(
    name='virtagym-api',
    packages=['workout_management'],
    include_package_data=True,
    install_requires=[
        'flask', 'sqlalchemy', 'alembic'
    ],
)
