"""
This file exposes 'app' to the module.
"""

# SPDX-FileCopyrightText: 2023-present Robin van der Noord <robinvandernoord@gmail.com>
#
# SPDX-License-Identifier: MIT

from rich import print  # noqa: import is there for library reasons

from .cli import app  # noqa: import is there for library reasons
from .core import (  # noqa: import is there for library reasons
    GREEN_CIRCLE,
    RED_CIRCLE,
    print_json,
    state,
)

# for plugins:
from .plugins import (  # noqa: import is there for library reasons
    register as register_plugin,
)
from .plugins import run_tool  # noqa: import is there for library reasons
