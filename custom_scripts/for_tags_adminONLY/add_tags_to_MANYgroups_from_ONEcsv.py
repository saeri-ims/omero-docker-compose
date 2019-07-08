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

# this script allows importing tags to many groups althought the csv file (with the tag names) has been attached to system group only
#the recommandation is that ADMIN is always member of the various groups
client = scripts.client(
    "add_tags_to_MANYgroups_from_ONEcsv.py",
    ("Customised script for adding tags from imported csv"),

    scripts.Long("File_Annotation"),

)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
print script_params


# get the 'IDs' parameter of the csv file imported as annotation

file_id = script_params["File_Annotation"]
file_ann = conn.getObject("FileAnnotation", file_id)
csv_text = "".join(list(file_ann.getFileInChunks()))
print csv_text
lines = csv_text.split("\n")
print lines

#check tags in all groups
for g in conn.getObjects("ExperimenterGroup"):
    conn.SERVICE_OPTS.setOmeroGroup(g.id)
    if g.id < 3 or "public" in g.name:   #this is important because i am not going to add tags to system, guest group and also not to any public group
        continue

    data = []

    col_names = lines[0]

    name_index = 0
    desc_index = 1


    for l in lines[1:]:
        cols = l.split(",")
        print cols
        if len(cols) < 1:
            continue
        text = cols[name_index]
        tags = list(conn.getObjects("TagAnnotation", attributes={"textValue": text}))
        if len(tags) > 0:
            print "Tag '%s' already exists" % text
            continue
        tag_ann = omero.gateway.TagAnnotationWrapper(conn)
        tag_ann.setValue(text)
        if len(cols) > 1:
            tag_ann.setDescription(cols[desc_index])
        tag_ann.save()



# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
