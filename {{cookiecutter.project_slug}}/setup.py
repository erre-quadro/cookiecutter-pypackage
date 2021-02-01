from setuptools import setup, find_packages
from {{ cookiecutter.project_slug }} import _about

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = open("requirements.txt").read().splitlines()

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

{%- set license_classifiers = {
    "Apache Software License 2.0": "License :: OSI Approved :: Apache Software License",
} %}

setup(
    author=_about.__author__,
    author_email=_about.__email__,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
{%- if cookiecutter.select_license in license_classifiers %}
        "{{ license_classifiers[cookiecutter.select_license] }}",
{%- endif %}
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description=_about.__summary__,
    install_requires=requirements,
{%- if cookiecutter.select_license in license_classifiers %}
    license="{{cookiecutter.select_license}}",
{%- endif %}
    long_description=readme,
    include_package_data=True,
    keywords=_about.__title__,
    name=_about.__title__,
    packages=find_packages(include=[_about.__title__, f"{_about.__title__}.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url=f"https://github.com/{{ cookiecutter.github_username }}/{_about.__title__}",
    version=_about.__version__,
    zip_safe=False,
)
