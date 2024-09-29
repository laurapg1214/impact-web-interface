from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION='OWB Python package'
LONG_DESCRIPTION='Objects Without Borders Python package for OWB project web interface, built for Bath Spa University, UK 2024'

setup(
    name="owb_module",
    version=VERSION,
    author="Laura Purcell-Gates",
    author_id="laurapg1214",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python',
        'pandas'
    ]
)