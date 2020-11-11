from distutils.core import setup

import setuptools

setup(
    name="shopper_payments_integration",
    version="0.4dev2",
    packages=setuptools.find_packages(),
    license="",
    long_description=open("README.md").read(),
    install_requires=[
        "Flask==1.1.2",
        "pytest==6.1.1",
        "requests==2.21.0",
        "six==1.15.0",
        "Flask-Caching==1.8",
        "sentry-sdk==0.14.0",
        "redis==3.5.3",
        "python-redis-lock==3.6.0",
    ],
)
