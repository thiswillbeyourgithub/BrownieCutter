
# BrownieCutter
* I just needed a quick script to lower the time cost of creating new FOSS tools. So just run this script, give the project name and class name and you'll get a proper template dir with some boiletplate code done for you.
* Yes BrownieCutter was created by itself.
* Inspired by [CookieCutter](https://cookiecutter.readthedocs.io/).

# Getting started
* As an uv tool: `uvx BrownieCutter@latest --help`
* From pypi: `uv pip install BrownieCutter` or `pip install BrownieCutter`
* From git: git clone then `pip install .`
* `BrownieCutter --help`


### Roadmap
<i>This TODO list is maintained automatically by [MdXLogseqTODOSync](https://github.com/thiswillbeyourgithub/MdXLogseqTODOSync)</i>
<!-- BEGIN_TODO -->
- add arg "requirements_source" to automatically populate the setup.py with them
- store the file content as fulltext in a source dir instead of in a var
- add arg "add to root"
    - which automatically overwrites (copy not move) placeholders with what's given, for example to give a LICENSE.md
- add arg "add to project dir"
    - for example used to copy  the utils dir directly at the right location
- add args to import code directly from a python file
    - use ast to match the imports line at the top
        - if there is a version number, automatically set it to this number
<!-- END_TODO -->

