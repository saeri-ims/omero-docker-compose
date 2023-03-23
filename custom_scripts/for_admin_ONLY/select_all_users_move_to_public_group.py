#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2014 University of Dundee & Open Microscopy Environment.
#                    All Rights Reserved.
# Use is subject to license terms supplied in LICENSE.txt
#

"""
FOR TRAINING PURPOSES ONLY!
"""

# This is a 'bare-bones' template to allow easy conversion from a simple
# client-side Python script to a script run by the server, on the OMERO
# scripting service.
# To use the script, simply paste the body of the script (not the connection
# code) into the point indicated below.
# A more complete template, for 'real-world' scripts, is also included in this
# folder
# This script takes an Image ID as a parameter from the scripting service.
from omero.rtypes import rlong, rstring, unwrap, robject
from omero.gateway import BlitzGateway, MapAnnotationWrapper
from omero.constants.metadata import NSCLIENTMAPANNOTATION
from omero.model import ExperimenterI, ExperimenterGroupI
import omero.scripts as scripts
import omero

import os


# Script definition

# Script name, description and 2 parameters are defined here.
# These parameters will be recognised by the Insight and web clients and
# populated with the currently selected Image(s)

# this script only takes all users
client = scripts.client(
    "select_users_move_to_public_group.py",
    ("Customised script for selecting users and adding them to the public domain group"),
)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
print(script_params)

# Use 'client' namespace to allow editing in Insight & web

namespace = NSCLIENTMAPANNOTATION

# list users with the 'IDs' parameter
#exp_id = script_params["Experimenter"]
experimenters = conn.getObjects("Experimenter")
exp_ids = []

for e in experimenters:
    print(e.id, e.firstName, e.lastName)
    if e.id > 1:
        exp_ids.append(e.id)

print("list ids", exp_ids)


# move users to a single object, in this case public domain

public_group_id = 5
adminService = conn.getAdminService()

for eid in exp_ids:
    adminService.addGroups(ExperimenterI(eid, False), [ExperimenterGroupI(public_group_id, False)])


# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
