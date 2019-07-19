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
data_types = [rstring('Dataset'),rstring('Image')]
client = scripts.client(
    "copy_tags_2kvpairs_per_selected_objects.py",
    ("Customised script for copying tags to kvpairs for selected objects"),
    # first parameter
    scripts.String(
        "Data_Type", grouping="1", optional=False, values=data_types, default="Dataset"),
    # second parameter
    scripts.List("IDs", grouping="2", optional=False).ofType(rlong(0)),
    # third parameter
    scripts.Bool("Copy_tags_on_object", grouping="3", description="object is the selected item", default=True),
    # fourth parameter
    scripts.Bool("Copy_tags_on_children", grouping="4", description="children is the list of objects within the selected item: e.g. images within selected dataset"),
)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
copy_self = script_params.get('Copy_tags_on_object', False)
copy_children = script_params.get('Copy_tags_on_children', False)
data_type = script_params['Data_Type']
print script_params

# Use 'client' namespace to allow editing in Insight & web

namespace = "kvpairs.from.tags.script"

# get the 'IDs' parameter (which we have restricted to 'Dataset' IDs)
ids = unwrap(client.getInput("IDs"))
ns = script_params["Namespace_text"]
ns = ns.strip()
#file_ns = conn.getObject("Namespace")  #is this necessary?
objects = conn.getObjects(data_type, ids)

#crete the list of annotation for the image
to_delete = []

#loop for looking at data in project/datasets and images
if data_type == 'Dataset':
    for ds in objects:
        if copy_children:
            to_delete.extend(list(ds.listChildren()))
        if copy_self:
            to_delete.append(ds)
else:
    to_delete = objects


for obj in to_delete:
    print obj.getId()
    ann_ids = []
    if ns == "none":
        ns = None
    for a in obj.listAnnotations(ns):
        #if a.OMERO_TYPE == given_type:
        print a.getId(), a.OMERO_TYPE, a.ns
        ann_ids.append(a.id)
    if len(ann_ids) > 0:
        print "Deleting %s annotations..." % len(ann_ids)
        conn.deleteObjects('Annotation', ann_ids, wait=True)

################
for d in datasets:
    print d.name

    tag_values = []

    for ann in d.listAnnotations():
        if isinstance(ann, omero.gateway.TagAnnotationWrapper):
            tag_values.append(ann.textValue)

    print "list tags", tag_values

    key_values = []

    for index, value in enumerate(tag_values):
        key_values.append([str(index), value])

    print "list kvs", key_values


    to_delete = []
    for ann in d.listAnnotations(ns=namespace):
        kv = ann.getValue()
        to_delete.append(ann.id)


    map_ann = omero.gateway.MapAnnotationWrapper(conn)
    map_ann.setNs(namespace)
    map_ann.setValue(key_values)
    map_ann.save()
    d.linkAnnotation(map_ann)

    if len(to_delete) > 0:
        conn.deleteObjects('Annotation', to_delete)

##################

# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
