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
#from omero.constants.metadata import NSCLIENTMAPANNOTATION
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
    "add_metadata19115_to_kvpairs_in_dataset.py",
    ("Customised script for adding the metadata form (ISO19115) to a dataset from imported csv. Note that the kvpairs will not be editable afterwards."),
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
print "script parameters", script_params


# Define namespace to not allow editing in Insight & web

namespace = "metadata19115file.from.csv"

# otherwise if kvpairs want to be kept editable
# Use 'client' namespace to allow editing in Insight & web

#namespace = NSCLIENTMAPANNOTATION

# get the 'IDs' parameter (which we have restricted to 'Dataset' IDs)
ids = unwrap(client.getInput("IDs"))
datasets = conn.getObjects("Dataset", ids)
file_id = script_params["File_Annotation"]
file_ann = conn.getObject("FileAnnotation", file_id)
csv_text = "".join(list(file_ann.getFileInChunks()))
print "csv text", csv_text
lines = csv_text.split("\n")
print "csv lines", lines

for ds in datasets:
    print "dataset names", ds

    owner = obj.getOwner().getName() #this line has been introduced to allow sysadmin to copy kvpairs on behalf of the owner's image
    data = []
    for l in lines:
        kv = l.split(",", 1)
        print "key values", kv
        if len(kv) == 2:
            data.append(kv)
        elif len(kv) == 1:
            data.append([kv[0], ""])

# create the object list to delete (in our case the annotations with a specific namespace)
    to_delete = []
    for ann in ds.listAnnotations(ns=namespace):
        kv = ann.getValue()
        to_delete.append(ann.id)


# only link a client map annotation to a single object

for dataset in conn.getObjects("Dataset", ids):
    #map_ann = omero.gateway.MapAnnotationWrapper(conn) #this line has been commented and superseeded by the line below in order to make the owner of the image also the owner of the new kvpairs
    suconn = conn.suConn(owner)  #this line has been introduced to allow sysadmin to copy kvpairs on behalf of the owner's image
    map_ann.setNs(namespace)
    map_ann.setValue(data)
    map_ann.save()
    dataset.linkAnnotation(map_ann)
    suconn.close()    #this line is necessary to "close" also the connection as "other user" as the sysadmin is now concluding to operate on behalf of the owner of the image

    if len(to_delete) > 0:
        conn.deleteObjects('Annotation', to_delete)


# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
