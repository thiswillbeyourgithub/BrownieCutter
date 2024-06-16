import sys
from pathlib import Path, PosixPath
import fire
from typeguard import typechecked
import os

class BrownieCutter:
    VERSION: str = "0.1.7"

    @typechecked
    def __init__(self) -> None:
        """
        Docstring can be found at self.create.__doc__
        """
        pass

    def create(
        self,
        project_name: str,
        project_class: str = None,
        verbose: bool=True,
        create_git: bool = True,
        create_pyenv: bool = True,
        ) -> None:
        """
        Create a new project directory with the specified structure and files.

        Parameters:
        -----------
        - project_name (str): The name of the project directory to be created. This will also be used as the default class name if `project_class` is not provided.

        - project_class (str, optional): The name of the main class for the project. Defaults to the value of `project_name`. Must be a valid Python class name (no spaces, starts with a letter).

        - verbose (bool, optional): If True, prints progress messages. Defaults to True.

        - create_git (bool, optional): If True, initializes a git repository in the project directory. Defaults to True.

        - create_pyenv: create a new virtual env using pyenv with name bc_{project_name} Automatically activate it using .env and .env.leave files (thanks to autoenv).
        """

        if verbose:
            self.p = self.printer
        else:
            self.p = self.fake_printer
        if project_class is None:
            project_class = project_name

        assert " " not in project_class, "no space can exist in the class name"
        assert project_class[0].isalpha(), "project class must be a valid class name"

        project = Path(project_name)
        assert not project.exists(), f"Dir already found: '{project}'"

        self.create_dir(project)

        src = project / project_name
        self.create_dir(src)

        self.create_file(
            project / "LICENSE.md",
            content="TODO_license",
        )

        self.create_file(
            project / "README.md",
            content=(
f'''
# {project_name}
TODO_introduction

# Getting started
* ` python -m pip install -e .`
TODO_tutorial
'''
            )
        )

        # fstring fix
        version = "{version}"
        old_version = "{old_version}"
        new_version = "{new_version}"

        self.create_file(
            project / "bumpver.toml",
            content=(
f'''
[bumpver]
current_version = "0.0.1"
version_pattern = "MAJOR.MINOR.PATCH"
commit_message = "bump version {old_version} -> {new_version}"
tag_message = "{new_version}"
tag_scope = "default"
commit = true
tag = true
push = false

[bumpver.file_patterns]
"bumpver.toml" = ['current_version = "{version}"']
"setup.py" = ['version="{version}"']
"{project_name}/{project_name}.py" = ['VERSION: str = "{version}"']

'''
            )
        )

        self.create_file(
            project / "setup.py",
            content=(
'''
from setuptools import setup, find_packages
from setuptools.command.install import install

with open("README.md", "r") as readme:
    long_description = readme.read()


setup(
    name="{project_name}",
    version="0.0.1",
    description="TODO_description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="TODO_URL",
    packages=find_packages(),

    # TODO_check_values
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GPLv3",
    keywords=[],
    python_requires=">=3.11",

    entry_points={
        'console_scripts': [
            '{project_name}={project_name}.__init__:cli_launcher',
        ],
    },

    install_requires=[
        "fire >= 0.6.0",
        "typeguard >= 0.4.3",
        # TODO_req
    ],
    extra_require={
    'optionnal_feature': [
        # TODO_req
        ]
    },

)
'''.replace("{project_name}", project_name)
            )
        )

        self.create_file(
                src / "__main__.py",
                content=(
f'''
from . import cli_launcher

if __name__ == "__main__":
    cli_launcher()
'''.strip()
            )
        )

        self.create_file(
                src / "__init__.py",
                content=(
f'''
import fire

from .{project_name} import {project_class}

def cli_launcher() -> None:
    fire.Fire({project_class})

if __name__ == "__main__":
    cli_launcher()
'''.strip()
            )
        )

        proj_file = src / (project_name + ".py")
        self.create_file(
                proj_file,
                content=(
f'''
from typeguard import typechecked

# TODO_imports

class {project_class}:
    VERSION: str = "0.1.7"

    @typechecked
    def __init__(
        self,
        ) -> None:\n
        """
        # TODO_docstring
        """

    TODO_code
'''.strip()
            )
        )

        if create_git:
            self.create_file(
                project / ".gitignore",
                content=(
f'''
**/*pycache*
**/*egg-info*

TODO_gitignore
'''
                )
            )
            try:
                self.p("Init git dir")
                to_add = f".gitignore README.md setup.py LICENSE.md bumpver.toml {project_name}"
                os.system(f"cd {project_name} && git init && git add {to_add} && git commit -m 'First commit (via BrownieCutter)'")
            except Exception as err:
                print(f"Couldn't init git dir: '{err}'")

        if create_pyenv:
            env_name = "bc_" + project_name.replace(" ", "_")
            os.system(f"cd {project_name} && pyenv virtualenv {sys.version.split(' ')[0]} {env_name} && touch .env .env.leave && pyenv activate {env_name} && python -m pip install build")
            if (project / ".env").exists() and (project / ".env.leave").exists():
                self.create_file(
                    project / ".env",
                    content=f"pyenv activate {env_name}",
                    create=True,
                )
                self.create_file(
                    project / ".env.leave",
                    content="pyenv deactivate",
                    create=True,
                )
            else:
                print(f"No {project_name}/.env file and .env.leave file found, assuming pyenv creation failed.")

        print(f"\nDone creating {project_name}, you can now manually replace all the missing TODO.")

        return


    @typechecked
    def printer(self, string: str) -> None:
        print(string)

    @typechecked
    def fake_printer(self, string: str) -> None:
        return

    @typechecked
    def create_dir(self, path: PosixPath) -> None:
        self.p(f"Creating dir '{path}'")
        path.mkdir(exist_ok=False)

    @typechecked
    def create_file(self, path: PosixPath, content: str, create: bool = False) -> None:
        self.p(f"Creating file '{path}'")
        path.touch(exist_ok=create)
        if content:
            path.write_text(content)



if __name__ == "__main__":
    fire.Fire(BrownieCutter().create)
