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
import omero.scripts as scripts
import omero

import os
import csv


# Script definition

# Script name, description and parameters are defined here.
# These parameters will be recognised by the Insight and web clients and
# populated with the currently selected Image(s)

# this script only takes all tags (project, datasets, images)
client = scripts.client(
    "add_checked_tags_and_change_ownership.py",
    ("Customised script for adding checked tags and changing tags' ownership"),
    scripts.Long("File_Annotation"),

)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
print script_params

#check tags in all groups
conn.SERVICE_OPTS.setOmeroGroup('-1')

# get the 'IDs' parameter of the tags
file_id = script_params["File_Annotation"]
file_ann = conn.getObject("FileAnnotation", file_id)
csv_text = "".join(list(file_ann.getFileInChunks()))
print csv_text
lines = csv_text.split("\n")
print lines
data = []

col_names = lines[0]

#get first the user ID as we want to search only for the tags that do not belong to the user id which is the admin
myOwnerId = conn.getUserId()
print 'myOwnerId', myOwnerId

name_index = 0
desc_index = 1

for l in lines[1:]:
    conn.SERVICE_OPTS.setOmeroGroup('-1')
    cols = l.split(",")
    print cols
    if len(cols) < 3:
        continue
    text = cols[name_index]
    tag_id = cols[2]
    tag_ann = conn.getObject("TagAnnotation", tag_id)
    tag_ann.setValue(text)
    gid = tag_ann.getDetails().group.id.val
    tag_ann._obj.details.owner = omero.model.ExperimenterI(myOwnerId, False)
    conn.SERVICE_OPTS.setOmeroGroup(gid)
    if len(cols) > 1:
        tag_ann.setDescription(cols[desc_index])
    tag_ann.save()



# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
