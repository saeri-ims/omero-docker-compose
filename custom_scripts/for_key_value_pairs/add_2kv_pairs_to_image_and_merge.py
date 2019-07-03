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

# Script name, description and 2 parameters are defined here.
# These parameters will be recognised by the Insight and web clients and
# populated with the currently selected Image(s)

# this script only takes Images
data_types = [rstring('Image')]
client = scripts.client(
    "add_2keys_and_values_to_an_image_and_merge.py",
    ("Customised script for adding 2 key_values pairs to an image and merge any previous map annotation"),
    # first parameter
    scripts.String(
        "Data_Type", grouping="1", optional=False, values=data_types, default="Image"),
    # second parameter
    scripts.List("IDs", grouping="2", optional=False).ofType(rlong(0)),
    scripts.String("First_key", grouping="3", default=""),
    scripts.String("First_value", grouping="4", default=""),
    scripts.String("Second_key", grouping="5", default=""),
    scripts.String("Second_value", grouping="6", default=""),
)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
print script_params

namespace = omero.constants.metadata.NSCLIENTMAPANNOTATION

# get the 'IDs' parameter (which we have restricted to 'Image' IDs)
ids = unwrap(client.getInput("IDs"))
images = conn.getObjects("Image", ids)

first_k = script_params["First_key"]
first_v = script_params["First_value"]
second_k = script_params["Second_key"]
second_v = script_params["Second_value"]

for i in images:
    print i.name
    key_value_data = []

    to_delete = []
    for ann in i.listAnnotations(ns=namespace):
        kv = ann.getValue()
        key_value_data.extend(kv)
        to_delete.append(ann.id)

    key_value_data.extend([[first_k, first_v], [second_k, second_v]])
    map_ann = omero.gateway.MapAnnotationWrapper(conn)
    map_ann.setNs(namespace)
    map_ann.setValue(key_value_data)
    map_ann.save()
    i.linkAnnotation(map_ann)

    if len(to_delete) > 0:
        conn.deleteObjects('Annotation', to_delete)

    print key_value_data

# Use 'client' namespace to allow editing in Insight & web

# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
