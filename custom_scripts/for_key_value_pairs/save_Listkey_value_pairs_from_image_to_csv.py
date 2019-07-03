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



# Script definition

# Script name, description and 2 parameters are defined here.
# These parameters will be recognised by the Insight and web clients and
# populated with the currently selected Image(s)

# this script only takes Images
data_types = [rstring('Image')]
client = scripts.client(
    "save_listkv_pairs_from_image_to_csv.py",
    ("Customised script for saving a list of key_values pairs from selected images to csv file"),
    # first parameter
    scripts.String(
        "Data_Type", grouping="1", optional=False, values=data_types, default="Image"),
    # second parameter
    scripts.List("IDs", grouping="2", optional=False).ofType(rlong(0)),
    scripts.List("New_keys", grouping="3", optional=False).ofType(rstring("")),
    scripts.List("New_values", grouping="4", optional=False).ofType(rstring("")),

)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
print script_params

# Use 'client' namespace to allow editing in Insight & web
namespace = NSCLIENTMAPANNOTATION

# get the 'IDs' parameter (which we have restricted to 'Image' IDs)
ids = unwrap(client.getInput("IDs"))
images = conn.getObjects("Image", ids)
keys = unwrap(client.getInput("New_keys"))
values = unwrap(client.getInput("New_values"))

with open("export_annotation.csv", "w") as f:
    for i in images:
        print i.name
        key_value_data = []

        to_delete = []
        for ann in i.listAnnotations(ns=namespace):
            kv = ann.getValue()
            key_value_data.extend(kv)
            to_delete.append(ann.id)

        key_value_data.extend([keys, values])
        map_ann = omero.gateway.MapAnnotationWrapper(conn)
        map_ann.setNs(namespace)
        map_ann.setValue(key_value_data)
        map_ann.save()
        i.linkAnnotation(map_ann)

        if len(to_delete) > 0:
            conn.deleteObjects('Annotation', to_delete)

        print key_value_data, '\n'
        f.write(i.name)
        f.write(kv)
        f.write('\n')


file_ann = conn.createFileAnnfromLocalFile("export_annotation.csv", mimetype="text/csv", ns="image.names.foo")
image = conn.getObject("Image", ids[0])
image.linkAnnotation(file_ann)

# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
