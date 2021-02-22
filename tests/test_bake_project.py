import os
import shlex
import subprocess
from contextlib import contextmanager

from cookiecutter.utils import rmtree


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def run_inside_dir(commands, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param commands: Commands that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        for command in commands:
            subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "setup.py" in found_toplevel_files
        assert "python_boilerplate" in found_toplevel_files
        assert "tests" in found_toplevel_files


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir(["pytest"], str(result.project)) == 0


def test_bake_with_specialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break setup.py"""
    with bake_in_temp_dir(
        cookies, extra_context={"full_name": 'name "quote" name'}
    ) as result:
        assert result.project.isdir()
        run_inside_dir(["pytest"], str(result.project)) == 0


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break setup.py"""
    with bake_in_temp_dir(
        cookies, extra_context={"full_name": "O'connor"}
    ) as result:
        assert result.project.isdir()
        run_inside_dir(["pytest"], str(result.project)) == 0


def test_bake_selecting_license(cookies):
    license = "Apache Software License 2.0"
    target = "Licensed under the Apache License, Version 2.0"
    with bake_in_temp_dir(
        cookies, extra_context={"select_license": license}
    ) as result:
        assert target in result.project.join("LICENSE").read()
        assert license in result.project.join("setup.py").read()


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"select_license": "None"}
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "setup.py" in found_toplevel_files
        assert "LICENSE" not in found_toplevel_files
        assert "License" not in result.project.join("README.rst").read()


def test_using_pytest(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        # Test contents of test file
        test_file_path = result.project.join(
            "tests/test_python_boilerplate.py"
        )
        lines = test_file_path.readlines()
        assert "import pytest" in "".join(lines)
        # Test the test alias (which invokes pytest)
        run_inside_dir(["pytest"], str(result.project)) == 0


def test_using_azure_ci(cookies):
    test_options = {"y": lambda x, y: x in y, "n": lambda x, y: x not in y}
    for answer, eval_func in test_options.items():
        with bake_in_temp_dir(
            cookies, extra_context={"use_azure_ci": answer}
        ) as result:
            found_toplevel_files = [
                f.basename for f in result.project.listdir()
            ]
            assert eval_func("azure-pipelines.yml", found_toplevel_files)


def test_using_cython(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"use_cython": "y"}
    ) as result:
        assert (
            "cython"
            in result.project.join("requirements-dev.txt").read().splitlines()
        )
        assert (
            "from Cython.Build import cythonize"
            in result.project.join("setup.py").read().splitlines()
        )
