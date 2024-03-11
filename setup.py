from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='AI fairytale',
    version='1.0',
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements
)
