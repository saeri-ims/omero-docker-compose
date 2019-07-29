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
data_types = [rstring('Dataset'),rstring('Image')]
client = scripts.client(
    "add_kv_pairs_from_csv_per_selected_objects.py",
    ("Customised script for adding key_values pairs to the selected objects (datasets and/or images) from imported csv. Note that the kvpairs will not be editable afterwards."),
    # first parameter
    scripts.String(
        "Data_Type", grouping="1", optional=False, values=data_types, default="Dataset"),
    # second parameter
    scripts.List("IDs", grouping="2", optional=False).ofType(rlong(0)),
    # third parameter
    scripts.String("File_Annotation", grouping="3", default=""),
    #scripts.Long("File_Annotation", grouping="3", default=""),
    # fourth parameter
    scripts.Bool("Add_kvpairs_to_object", grouping="4", description="object is the selected item", default=True),
    # fifth parameter
    scripts.Bool("Add_kvpairs_to_children", grouping="5", description="children is the list of objects within the selected item: e.g. images within selected dataset"),

)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
add_self = script_params.get('Add_kvpairs_to_object', False)
add_children = script_params.get('Add_kvpairs_to_children', False)
data_type = script_params['Data_Type']
print script_params


# Define namespace to not allow editing in Insight & web

namespace = "kvpairs.from.csv"

# otherwise if kvpairs want to be kept editable
# Use 'client' namespace to allow editing in Insight & web

#namespace = NSCLIENTMAPANNOTATION

# get the 'IDs' parameter (will match the id of the selected object to which the csv file has been attached)
ids = unwrap(client.getInput("IDs"))

file_id = script_params["File_Annotation"]
file_ann = conn.getObject("FileAnnotation", file_id)
csv_text = "".join(list(file_ann.getFileInChunks()))
print csv_text
lines = csv_text.split("\n")
print lines


#connect to the object
objects = conn.getObjects(data_type, ids)
print "objects", objects

#create the list of the objects (Datasets, images or both)
object_list = []

#loop for looking at data in project/datasets and images
if data_type == 'Dataset':
    for ds in objects:
        if add_children:
            object_list.extend(list(ds.listChildren()))
        if add_self:
            object_list.append(ds)
else:
    object_list = objects

print object_list

for obj in object_list:

    owner = obj.getOwner().getName() #this line has been introduced to allow sysadmin to copy kvpairs on behalf of the owner's image

    data = []
    for l in lines:
        kv = l.split(",", 1)
        print kv
        if len(kv) == 2:
            data.append(kv)
        elif len(kv) == 1:
            data.append([kv[0], ""])

    print "list data", data

    to_delete = []
    for ann in obj.listAnnotations(ns=namespace):
        kv = ann.getValue()
        to_delete.append(ann.id)

#for dataset in conn.getObjects("Dataset", ids):
    #map_ann = omero.gateway.MapAnnotationWrapper(conn) #this line has been commented and superseeded by the line below in order to make the owner of the image also the owner of the new kvpairs
    suconn = conn.suConn(owner)  #this line has been introduced to allow sysadmin to copy kvpairs on behalf of the owner's image
    map_ann = omero.gateway.MapAnnotationWrapper(suconn)
    map_ann.setNs(namespace)
    map_ann.setValue(data)
    map_ann.save()
    obj.linkAnnotation(map_ann)
    suconn.close()    #this line is necessary to "close" also the connection as "other user" as the sysadmin is now concluding to operate on behalf of the owner of the image

    if len(to_delete) > 0:
        conn.deleteObjects('Annotation', to_delete)

# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
