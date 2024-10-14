# Pyright-alright

![PyPI](https://img.shields.io/pypi/v/pyright-alright)
![Supported python versions](https://img.shields.io/pypi/pyversions/pyright-alright)

**The pyright type checker, packaged for Python** 🍞 + 🐍 + 🪨 = 🚀 

[Pyright](https://github.com/microsoft/pyright) is a full-featured, standards-based static type checker for Python. It is designed for high performance and can be used with large Python source bases.

The [pyright-alright](https://pypi.org/project/pyright-alright/) Python package is a self-contained command-line wrapper over pyright that works out of the box: no need to install [node](https://github.com/nodejs/node).


Installation
------------

Use the package manager of your choice to install pyright-alright.

Here is a simple example with [pip](https://github.com/pypa/pip):

```shell
pip install pyright-alright
```

Usage
-----

### Command line

```shell
pyright --version

# Alternatives
pyright-alright --version
pyright_alright --version
```

### Run library module as a script

```shell
python -m pyright_alright --version
```

### As a pre-commit hook

```yaml

repos:
  - repo: local
    hooks:
      - id: pyright
        name: Run pyright
        entry: pyright
        language: system
        types: [file, python]
```

Documentation
-------------

To configure and use pyright properly, you should take time to read the [Pyright documentation](https://microsoft.github.io/pyright/#/).

Motivation
----------

**TL;DR**: self-contained, no runtime installation under the hood, no network calls, no warnings, just a pyright CLI.

Pyright is written in Typescript therefore it requires us to
install a Javascript package manager (ex: npm) and a Javascript Runtime (ex: node) to make it work.

It also makes it not possible to track the pyright's version of a project in your `pyproject.toml` or your `requirements.txt` like any other dependencies. 

There is already [pyright-python](https://github.com/RobertCraigie/pyright-python), a community-maintained command-line wrapper over pyright, which works well but it has drawbacks.

Until [until recently](https://github.com/RobertCraigie/pyright-python/commit/e2d0748d4afe19a3af78b58422dba11a631484a7) it required to either have node installed or it would
automatically download node when running the CLI for the first time.

This default behaviour led to annoying bugs in my company's CI server.

Moreover, it prints a warning every time it detects that that a new version is available which I find to be an annoying default configuration.

```shell
$ pyright
WARNING: there is a new pyright version available (v1.1.371 -> v1.1.384).
Please install the new version or set PYRIGHT_PYTHON_FORCE_VERSION to `latest`
```

[pyright-alright](https://github.com/ducdetronquito/pyright-alright) is not a revolution at all but provides good defaults:

- No need to install npm/nodejs thanks to [pybun](https://github.com/ducdetronquito/pybun) which packages the [bun](https://bun.sh) Javascript runtime to make pyright works
- No installation or network calls is done when running the CLI
- No unwanted warnings about new pyright version available
- Just a working pyright CLI
