#!/usr/bin/env python

#
# Copyright (c) 2024 University of Dundee.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys

from omero.cli import CLI
from omero_annotation_scripts import HELP, Annotation_scriptsControl

try:
    register("annotation_scripts", Annotation_scriptsControl, HELP)  # type: ignore
except NameError:
    if __name__ == "__main__":
        cli = CLI()
        cli.register("annotation_scripts", Annotation_scriptsControl, HELP)
        cli.invoke(sys.argv[1:])
