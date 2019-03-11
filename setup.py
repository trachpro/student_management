from setuptools import setup, find_packages

setup(
    name='student_management',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'requests',
        'PyJWT',
        'marshmallow',
        'PyMySQL',
        'passlib'
    ],
)