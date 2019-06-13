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

# Script name, description and 2 parameters are defined here.
# These parameters will be recognised by the Insight and web clients and
# populated with the currently selected Image(s)

# this script only takes Datasets
data_types = [rstring('Dataset')]
client = scripts.client(
    "add_keys_and_values_to_a_dataset_from_csv.py",
    ("Customised script for adding key_values pairs to a dataset from imported csv"),
    # first parameter
    scripts.String(
        "Data_Type", grouping="1", optional=False, values=data_types, default="Dataset"),
    # second parameter
    scripts.List("IDs", grouping="2", optional=False).ofType(rlong(0)),
    scripts.String("File_Annotation", grouping="3", default=""),
    #scripts.Long("File_Annotation", grouping="3", default=""),

)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
print script_params

# Use 'client' namespace to allow editing in Insight & web

namespace = NSCLIENTMAPANNOTATION

# get the 'IDs' parameter (which we have restricted to 'Dataset' IDs)
ids = unwrap(client.getInput("IDs"))

file_id = script_params["File_Annotation"]  #question why not simply file_id= File_Annotation?
file_ann = conn.getObject("FileAnnotation", file_id)
csv_text = "".join(list(file_ann.getFileInChunks()))
print csv_text
lines = csv_text.split("\n")
print lines
data = []

for l in lines:
    kv = l.split(",", 1)
    print kv
    if len(kv) == 2:
        data.append(kv)
    elif len(kv) == 1:
        data.append([kv[0], ""])

# data = [l.split(",") for l in lines]



# only link a client map annotation to a single object

for dataset in conn.getObjects("Dataset", ids):
    map_ann = omero.gateway.MapAnnotationWrapper(conn)
    map_ann.setNs(namespace)
    map_ann.setValue(data)
    map_ann.save()
    dataset.linkAnnotation(map_ann)



# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
