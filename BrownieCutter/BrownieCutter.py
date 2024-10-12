import sys
from pathlib import Path, PosixPath
import fire
from beartype import beartype
import os

@beartype  # this will apply to all methods
class BrownieCutter:
    VERSION: str = "0.1.14"

    def __init__(self) -> None:
        """
        Docstring can be found at self.create.__doc__
        """
        pass

    def create(
        self,
        project_name: str,
        classname: str = None,
        verbose: bool = True,
        create_git: bool = True,
        create_venv: str = "uv",
        typechecking: bool = True,
        ) -> None:
        """
        Create a new project directory with the specified structure and files.

        Parameters:
        -----------
        - project_name (str): The name of the project directory to be created. This will also be used as the default class name if `classname` is not provided.

        - classname (str, optional): The name of the main class for the project. Defaults to the value of `project_name`. Must be a valid Python class name (no spaces, starts with a letter).

        - verbose (bool, optional): If True, prints progress messages. Defaults to True.

        - create_git (bool, optional): If True, initializes a git repository in the project directory. Defaults to True.

        - create_venv (str, default 'uv'): create a new virtual env using uv with name bc_{project_name} Automatically activate it using .env and .env.leave files (thanks to autoenv). If set to 'pyenv' will use pyenv, otherwise will use 'uv'.

        - typechecking: automatically add beartype typechecking. Defaults to True.
        """

        if verbose:
            self.p = self.printer
        else:
            self.p = self.fake_printer
        if classname is None:
            classname = project_name

        assert " " not in classname, "no space can exist in the class name"
        assert classname[0].isalpha(), "project class must be a valid class name"

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
* From pypi:
    * As a tool: `uvx {project_name}@latest --help`  # TODO: can this be used as a tool?
    * Via uv: `uv pip install {project_name}`
    * Via pip: `pip install {project_name}`
* From github:
* Clone this repo then `pip install .`

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

        setup_content = '''
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
    keywords=["TODO_keywords"],
    python_requires=">=3.11",

    entry_points={
        'console_scripts': [
            '{project_name}={project_name}.__init__:cli_launcher',
        ],
    },

    install_requires=[
        'fire >= 0.6.0',
        'beartype >= 0.19.0',
        # TODO_req
    ],
    extra_require={
        'feature1': [
            # TODO_req
        ],
        'feature2': [
            # TODO_req
        ]
    },

)
'''
        setup_content = setup_content.replace("{project_name}", project_name)
        if not typechecking:
            setup_content = "".join(
                [
                    li
                    for li in setup_content.splitlines(keepends=True)
                    if "beatype" not in li
                ]
                )
        self.create_file(
            project / "setup.py",
            content=(
('''
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
    keywords=["TODO_keywords"],
    python_requires=">=3.11",

    entry_points={
        'console_scripts': [
            '{project_name}={project_name}.__init__:cli_launcher',
        ],
    },

    install_requires=[
        'fire >= 0.6.0',
        'beartype >= 0.18.5',
        # TODO_req
    ],
    extra_require={
    'feature1': [
        # TODO_req
        ],
    'feature2': [
        # TODO_req
        ]
    },

)
''').replace("{project_name}", project_name)
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
import sys
import fire

from .{project_name} import {classname}

__all__ = ["{classname}"]

__VERSION__ = {classname}.VERSION

def cli_launcher() -> None:
    if sys.argv[-1] ==  "--version":
        return(f"{project_name} version: ''' + "{__VERSION__}" + f'''")
    fire.Fire({classname})

if __name__ == "__main__":
    cli_launcher()
'''.strip()
            )
        )

        proj_file = src / (project_name + ".py")
        project_content = f'''
from beartype import beartype
# TODO_imports

@beartype  # this will apply to all methods
class {classname}:
    VER_IGNORE_SION: str = "0.0.1"

    def __init__(
        self,
        ) -> None:\n
        """
        # TODO_docstring
        """

# TODO_code
'''
        project_content = project_content.strip().replace(
                    "VER_IGNORE_SION",
                    "VERSION"
                )
        if not typechecking:
            project_content = "".join(
                [
                    li
                    for li in project_content.splitlines(keepends=True)
                    if "beatype" not in li
                ]
                )
        self.create_file(
                proj_file,
                content=project_content,
        )

        if create_git:
            self.create_file(
                project / ".gitignore",
                content=(
'''
**/*pycache*
**/*egg-info*
''' + ('' if not create_venv else '''
.env
.env.leave
''' ) + '''

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

        if create_venv == "pyenv":
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
        elif create_venv == "uv":
            env_name = "bc_" + project_name.replace(" ", "_")
            os.system(f"cd {project_name} && uv venv {env_name} --python {sys.version.split(' ')[0]} && touch .env .env.leave && source .venv/bin/activate && uv pip install build")
            if (project / ".env").exists() and (project / ".env.leave").exists():
                self.create_file(
                    project / ".env",
                    content=f"source .venv/bin/activate",
                    create=True,
                )
                self.create_file(
                    project / ".env.leave",
                    content="deactivate",
                    create=True,
                )
            else:
                print(f"No {project_name}/.env file and .env.leave file found, assuming uv venv creation failed.")
        elif not create_venv:
            print("No venv to create.")
        else:
            raise ValueError("The arg create_venv only accepts value 'pyenv' or 'uv'")

        print(f"\nDone creating {project_name}, you can now manually replace all the missing TODO.")

        return


    def printer(self, string: str) -> None:
        print(string)

    def fake_printer(self, string: str) -> None:
        return

    def create_dir(self, path: PosixPath) -> None:
        self.p(f"Creating dir '{path}'")
        path.mkdir(exist_ok=False)

    def create_file(self, path: PosixPath, content: str, create: bool = False) -> None:
        self.p(f"Creating file '{path}'")
        path.touch(exist_ok=create)
        if content:
            path.write_text(content)



if __name__ == "__main__":
    fire.Fire(BrownieCutter().create)
