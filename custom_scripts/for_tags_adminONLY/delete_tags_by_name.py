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


# Script definition

# Script name, description and 2 parameters are defined here.
# These parameters will be recognised by the Insight and web clients and
# populated with the currently selected Image(s)

# this script only takes Datasets
data_types = [rstring('Project'), rstring('Dataset'),rstring('Image')]
client = scripts.client(
    "remove_specified_tags_from_selected_objects.py",
    ("Customised script for removing specified tags (links) from selected objects"),
    # first parameter
    scripts.String(
        "Data_Type", grouping="1", optional=False, values=data_types, default="Dataset"),
    # second parameter
    scripts.List("IDs", grouping="2", optional=False).ofType(rlong(0)),
    # third parameter
    scripts.String("Tag_name", grouping="3", default=""),
    # fourth parameter
    scripts.Bool("Delete_Tags_on_object", grouping="4", description="object is the selected item"),
    # fifth parameter
    scripts.Bool("Delete_Tags_on_children", grouping="5", description="children is the list of objects within the selected item: e.g. images within selected dataset"),
)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
delete_self = script_params.get('Delete_Tags_on_object', False)
delete_children = script_params.get('Delete_Tags_on_children', False)
data_type = script_params['Data_Type']
print "script parameters", script_params


# get the 'IDs' parameter (which we have restricted to 'Dataset' IDs)
ids = unwrap(client.getInput("IDs"))
nametag = script_params["Tag_name"]
#the line below allows to add more than one tag name
tag_names = [x.strip() for x in nametag.split(',')]
objects = conn.getObjects(data_type, ids)



#create the list of the objects (Datasets, images or both)
object_list = []

#loop for looking at data in project/datasets and images
if data_type == 'Project':
    for p in objects:
        if delete_children:
            for ds in p.listChildren():
                object_list.extend(list(ds.listChildren()))
        if delete_self:
            object_list.append(ds)
elif data_type == 'Dataset':
    for ds in objects:
        if delete_children:
            object_list.extend(list(ds.listChildren()))
        if delete_self:
            object_list.append(ds)
else:
    object_list = objects

#create the annotation lists per object
link_to_delete_images = []
link_to_delete_projects = []
link_to_delete_datasets = []

for obj in object_list:
    # for each object load the annotation (append)
    for ann in obj.listAnnotations():
        if ann.OMERO_TYPE == omero.model.TagAnnotationI:
            if ann.getTextValue() in tag_names:
                if isinstance(obj, omero.gateway.ImageWrapper):
                    link_to_delete_images.append(ann.link.getId())
                elif isinstance(obj, omero.gateway.DatasetWrapper):
                    link_to_delete_datasets.append(ann.link.getId())
                elif isinstance(obj, omero.gateway.ProjectWrapper):
                    link_to_delete_projects.append(ann.link.getId())

#if there is a tag name in the object specific list, then delete
if len(link_to_delete_images) > 0:
    conn.deleteObjects("ImageAnnotationLink", link_to_delete_images)
if len(link_to_delete_datasets) > 0:
    conn.deleteObjects("DatasetAnnotationLink", link_to_delete_datasets)
if len(link_to_delete_projects) > 0:
    conn.deleteObjects("ProjectAnnotationLink", link_to_delete_projects)

# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
