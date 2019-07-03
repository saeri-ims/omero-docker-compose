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

# this script only takes tags
client = scripts.client(
    "merge_tags.py",
    ("Customised script for merging tags with the same names"),

)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
#search for tags in all the groups
conn.SERVICE_OPTS.setOmeroGroup('-1')

script_params = client.getInputs(unwrap=True)
print script_params


#create a list of tags and append only the tags, tag id and tag owner id to it
tags = []

for tag in conn.getObjects("TagAnnotation"):
    owner = tag.getDetails().owner.id.val
    print tag.textValue, owner
    tags.append([tag.textValue, str(tag.id), str(owner)])

#sort the tags in descending order to allow to see duplicates

tags.sort(key=lambda tag: tag[0].islower())

#in the listed tags check the duplicates and retain only the firts found and relink the images to this retained tag
prev_tag = ""
prev_id = 0
for t in tags:
    tag_id = str(t[1)  ##there is a mistake here
    if t[0] == prev_tag:
        # move all tagged objects to previous tags and delete
        for link in conn.getAnnotationLinks('Image', ann_ids=[tag_id]):
            link._obj.child = omero.model.TagAnnotationI(prev_id, False)
            link.save()
        conn.deleteObjects('TagAnnotation', [tag_id])
    prev_tad = t[0]
    prev_id = tag_id

# set group to save file to. NB: hard-coded as stystem group
conn.SERVICE_OPTS.setOmeroGroup('0')
file_ann = conn.createFileAnnfromLocalFile("tags_merged.csv", mimetype="text/csv", ns="tags.to.be.merged")  #this should be commented?



# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))
client.setOutput("File_Annotation", robject(file_ann._obj))

client.closeSession()
