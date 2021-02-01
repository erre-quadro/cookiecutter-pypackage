import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == "__main__":

    if "{{ cookiecutter.select_license }}" == "None":
        remove_file("LICENSE")

    if "{{ cookiecutter.include_azure_ci }}" == "n":
        remove_file("azure-pipelines.yml")
