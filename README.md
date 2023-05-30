# su6-checker

[![PyPI - Version](https://img.shields.io/pypi/v/su6.svg)](https://pypi.org/project/su6)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/su6.svg)](https://pypi.org/project/su6)

-----
su6 (6 is pronounced as '/zɛs/' in Dutch, so 'su6' is basically 'success')  
This package will hopefully help achieve that!

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Changelog](#changelog)

## Installation

```console
# quick install with all possible checkers:
pip install su6[all]
# or pick and choose checkers:
pip install [black,bandit,pydocstyle]
```

**Note**: this package does not work well with `pipx`, since a lot of the tools need to be in the same (virtual)
environment
of your code, in order to do proper analysis.

The following checkers are supported:

### ruff

- install: `pip install su6[ruff]`
- use: `su6 ruff [directory]`
- functionality: linter
- pypi: [ruff](https://pypi.org/project/ruff/)

### black

- install: `pip install su6[black]`
- use: `su6 black [directory] [--fix]`
- functionality: formatter
- pypi: [black](https://pypi.org/project/black/)

### mypy

- install: `pip install su6[mypy]`
- use: `su6 mypy [directory]`
- functionality: static type checker
- pypi: [mypy](https://pypi.org/project/mypy/)

### bandit

- install: `pip install su6[bandit]`
- use: `su6 bandit [directory]`
- functionality: security linter
- pypi: [bandit](https://pypi.org/project/bandit/)

### isort

- install: `pip install su6[isort]`
- use: `su6 isort [directory] [--fix]`
- functionality: import sorter
- pypi: [isort](https://pypi.org/project/isort/)

### pydocstyle

- install: `pip install su6[pydocstyle]`
- use: `su6 pydocstyle [directory]`
- functionality: docstring checker
- pypi: [pydocstyle](https://pypi.org/project/pydocstyle/)

### pytest

- install: `pip install su6[pytest]`
- use: `su6 pytest [directory] [--coverage <int>] [--json] [--html]`
- functionality: tester with coverage
- pypi: [pytest](https://pypi.org/project/pytest/), [pytest-cov](https://pypi.org/project/pytest-cov/)

## Usage

```console
su6 --help
# or, easiest to start:
su6 all
# usual signature:
su6 [--verbosity=1|2|3] [--config=...] <subcommand> [directory] [...specific options]
```

where `subcommand` is `all` or one of the available checkers;  
`verbosity` indicates how much information you want to see (default is '2').  
`config` allows you to select a different `.toml` file (default is `pyproject.toml`).  
`directory` is the location you want to run the scans (default is current directory);  
In the case of `black` and `isort`, another optional parameter `--fix` can be passed.
This will allow the tools to do the suggested changes (if applicable).
Running `su6 fix` will run both these tools with the `--fix` flag.  
For `pytest`, `--json`, `--html` and `--coverage <int>` are supported. The latter can also be configured in the
pyproject.toml (see ['Configuration'](#configuration)).
The first two arguments can be used to control the output format of `pytest --cov`. Both options can be used at the same
time. The `--coverage` flag can be used to set a threshold for code coverage %. If the coverage is less than this
threshold, the check will fail.

### Configuration

In your `pyproject.toml`, you can add a `[tools.su6]` section to configure some of the behavior of this tools.
Currently, the following keys are supported:

```toml
[tool.su6]
directory = "." # string path to the directory on which to run all tools, e.g. 'src'
include = [] # list of checks to run (when calling `su6 all`), e.g. ['black', 'mypy']
exclude = [] # list of checks to skip (when calling `su6 all`), e.g. ['bandit']
coverage = 100 # int threshold for pytest coverage 
```

All keys are optional. Note that if you have both an `include` as well as an `exclude`, all the tools in `include` will
run and `exclude` will be fully ignored.

### Github Action

In order to use this checker within Github to run checks after pushing,
you can add a workflow (e.g. `.github/workflows/su6.yaml`) like this example:

```yaml
name: run su6 checks
on:
  push:
    branches-ignore:
      - master
jobs:
  check:
    name: Check with `su6 all`
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip' # caching pip dependencies
      - run: pip install su6[all]
      - run: su6 all
```

**Note:** if you don't want to run all checks, but specific ones only, you need to add the `--ignore-uninstalled` flag
to `su6 all`! Otherwise, Github will see exit code 127 (command missing) as a failure.

```yaml
name: run some su6 checks
on:
  push:
    branches-ignore:
      - master
jobs:
  check:
    name: Check with `su6 all`
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip' # caching pip dependencies
      - run: pip install su6[pycodestyle,black]
      - run: su6 all --ignore-uninstalled
```

## License

`su6` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Changelog

See `CHANGELOG.md` [on GitHub](https://github.com/robinvandernoord/su6-checker/blob/master/CHANGELOG.md)
