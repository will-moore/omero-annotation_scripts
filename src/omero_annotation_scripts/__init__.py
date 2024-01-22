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

import os

from omero.model import OriginalFileI
from omero.gateway import BlitzGateway

from omero.cli import BaseControl, Parser

HELP = """pip installable OMERO.scripts for annotation workflows

    $ omero annotation_scripts upload

        This will upload the scripts to OMERO or replace them if they
        already exist.

"""


class Annotation_scriptsControl(BaseControl):
    def _configure(self, parser: Parser) -> None:
        parser.add_login_arguments()
        sub = parser.sub()
        parser.add(sub, self.upload, "Upload scripts to OMERO (must be Admin)")


    def upload(self, args):
        conn = BlitzGateway(client_obj=self.ctx.conn(args))
        if not conn.isAdmin():
            self.ctx.out("You need to be an Admin to upload scripts")
        script_path = os.path.dirname(os.path.abspath(__file__))
        scripts_dir = os.path.join(os.path.dirname(script_path), "scripts")

        for name in os.listdir(scripts_dir):
            print("Script name", name)
            path_to_script = os.path.join(scripts_dir, name)
            if os.path.isfile(path_to_script):
                script_text = None
                with open(path_to_script) as fhandle:
                    script_text = fhandle.read()
                if script_text is not None:

                    script_service = conn.getScriptService()
                    script_path = f"/omero/annotation_scripts/{name}"

                    # replace if script exists
                    script_id = script_service.getScriptID(script_path)
                    print("script ID", script_id)
                    if script_id > 0:
                        orig_file = OriginalFileI(script_id, False)
                        script_service.editScript(orig_file, script_text)
                        print("Script Replaced: %s" % script_id)
                    else:
                        script_id = script_service.uploadOfficialScript(
                            script_path, script_text)
                        print("Script Uploaded: %s" % script_id)

        self.ctx.out("Done.")
