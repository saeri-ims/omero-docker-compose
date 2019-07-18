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
import omero.scripts as scripts
import omero

import os


# Script definition

# Script name, description and parameters are defined here.
# These parameters will be recognised by the Insight and web clients and
# populated with the currently selected Image(s)

# this script only takes Images
data_types = [rstring('Image')]
client = scripts.client(
    "copy_tags_2kvpairs_per_images.py",
    ("Customised script for copying tags names to key_values pairs for each image"),

    scripts.String(
        "Data_Type", grouping="1", optional=False, values=data_types, default="Image"),

)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
print script_params

namespace = "kvpairs.from.tags.script"

# get the 'IDs' parameter (which we have restricted to 'Image' IDs)
ids = unwrap(client.getInput("IDs"))
image = conn.getObjects("Image", ids)


for i in image:
    print i.name

    tag_values = []

    for ann in i.listAnnotations():
        if isinstance(ann, omero.gateway.TagAnnotationWrapper):
            tag_values.append(ann.textValue)

    print "list tags", tag_values

    key_values = []

    for index, value in enumerate(tag_values):
        key_values.append([str(index), value])

    print "list kvs", key_values


    to_delete = []
    for ann in i.listAnnotations(ns=namespace):
        kv = ann.getValue()
        to_delete.append(ann.id)


    map_ann = omero.gateway.MapAnnotationWrapper(conn)
    map_ann.setNs(namespace)
    map_ann.setValue(key_values)
    map_ann.save()
    i.linkAnnotation(map_ann)

    if len(to_delete) > 0:
        conn.deleteObjects('Annotation', to_delete)


# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()