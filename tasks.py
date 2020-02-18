"""Development tasks for the cookiecutter template project"""

import platform
from pathlib import Path
from invoke import task

ROOT_DIR = Path(__file__).parent
DOCS_DIR = ROOT_DIR.joinpath('docs')
DOCS_BUILD_DIR = DOCS_DIR.joinpath('_build')
DOCS_INDEX = DOCS_BUILD_DIR.joinpath('index.html')
TEST_DIR = ROOT_DIR.joinpath('tests')
HOOKS_DIR = ROOT_DIR.joinpath('hooks')
PYTHON_DIRS = [str(HOOKS_DIR), str(TEST_DIR)]


@task(help={'check': "Checks if source is formatted without applying changes"})
def format(c, check=False):
    """
    Format code
    """
    python_dirs_string = " ".join(PYTHON_DIRS)

    # Run autoflake
    autoflake_options = [
        "--check" if check else "--in-place",
        "--ignore-init-module-imports",
        "--recursive",
        "--remove-all-unused-imports",
    ] 
    c.run("autoflake {} {}".format(" ".join(autoflake_options), python_dirs_string))
    
    # Run yapf
    yapf_options = "--recursive {}".format("--diff" if check else "--in-place")
    c.run("yapf {} {}".format(yapf_options, python_dirs_string))
    
    # Run isort
    isort_options = [
        "--check-only" if check else "",
        "--apply",
        "--combine-as",
        "--force-grid-wrap=0",
        "--line-width 79", # PEP 8 says 79.
        "--multi-line=3",
        "--recursive",
        "--trailing-comma",
    ]
    c.run("isort {} {}".format(" ".join(isort_options), python_dirs_string))

    # Run black
    black_options = [
        "--check" if check else "",
        "--line-length 79",
    ]
    c.run("black {} {}".format(" ".join(black_options), python_dirs_string))

    # Run vulture
    vulture_options = [
        "--min-confidence 70"
    ]
    c.run("vulture {} {}".format(" ".join(vulture_options), python_dirs_string))


@task
def lint(c):
    """
    Lint code
    """
    python_dirs_string = " ".join(PYTHON_DIRS)
    c.run("flake8 {}".format(python_dirs_string))
    c.run("pylint {}".format(python_dirs_string))


@task
def test(c):
    """
    Run tests
    """
    pty = platform.system() == 'Linux'
    c.run("pytest", pty=pty)


@task
def docs(c):
    """
    Generate documentation
    """
    c.run("sphinx-build -b html {} {}".format(DOCS_DIR, DOCS_BUILD_DIR))


@task
def clean_docs(c):
    """
    Clean up files from documentation builds
    """
    c.run("rm -fr {}".format(DOCS_BUILD_DIR))
