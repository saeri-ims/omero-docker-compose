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
#import csv

# Script definition

# Script name, description and 2 parameters are defined here.
# These parameters will be recognised by the Insight and web clients and
# populated with the currently selected Image(s)

# this script only takes Datasets
data_types = [rstring('Dataset')]
client = scripts.client(
    "remove_kv_pairs_from_dataset.py",
    ("Customised script for removing key_values pairs from a dataset"),
    # first parameter
    scripts.String(
        "Data_Type", grouping="1", optional=False, values=data_types, default="Dataset"),
    # second parameter
    scripts.List("IDs", grouping="2", optional=False).ofType(rlong(0)),
    # third parameter
    scripts.String("Namespace_text", grouping="3", default=""),
    #scripts.Long("File_Annotation", grouping="3", default=""),

)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
print script_params

# Use 'client' namespace to allow editing in Insight & web

#namespace = NSCLIENTMAPANNOTATION

# get the 'IDs' parameter (which we have restricted to 'Dataset' IDs)
ids = unwrap(client.getInput("IDs"))
ns = script_params["Namespace_text"]
#file_ns = conn.getObject("Namespace")  #is this necessary?
list_datasets = conn.getObjects("Dataset", ids)

for dataset in list_datasets:
    print dataset.getId()
    ann_ids = []
    given_type = None
    if anntype == "map":
        given_type = omero.model.MapAnnotationI
    #if anntype == "file":
        #given_type = omero.model.FileAnnotationI
    if ns == "none":
        ns = None
    for image in dataset.listChildren():
        for a in image.listAnnotations(ns):
            if a.OMERO_TYPE == given_type:
                print a.getId(), a.OMERO_TYPE, a.ns
                ann_ids.append(a.id)
    # Delete the annotations link to the dataset
    for a in dataset.listAnnotations(ns):
        if a.OMERO_TYPE == given_type:
            print a.getId(), a.OMERO_TYPE, a.ns
            ann_ids.append(a.id)
    if len(ann_ids) > 0:
        print "Deleting %s annotations..." % len(ann_ids)
        conn.deleteObjects('Annotation', ann_ids, wait=True)



# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
