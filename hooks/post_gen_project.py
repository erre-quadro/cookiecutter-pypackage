import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == "__main__":

    if "{{ cookiecutter.select_license }}" == "Not open source":
        remove_file("LICENSE")

    if "{{ cookiecutter.select_appveyor_ci }}" == "n":
        remove_file("appveyor.yml")

    if "{{ cookiecutter.select_travis_ci }}" == "n":
        remove_file(".travis.yml")
