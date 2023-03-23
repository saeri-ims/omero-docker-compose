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

# this script allows importing tags in the group where the csv file has been attached to
#the recommandation is that ADMIN is always member of a group and ADMIN creates a project called tags
data_types = [rstring('Dataset'), rstring('Image'), rstring('Project')]
client = scripts.client(
    "vocabulary_to_map_annotation.py",
    ("Customised script for looking-up kvpairs in a dictionary created from imported csv and add matching rows to key-value pairs"),

    scripts.Long("File_Annotation"),

    scripts.String(
        "Data_Type", optional=False, grouping="1",
        description="The data you want to work with.", values=data_types,
        default="Image"),

    scripts.List(
        "IDs", optional=False, grouping="2",
        description="List of Dataset IDs or Image IDs").ofType(rlong(0)),
    #define the position of the key in the csv file
    scripts.Int(
        "Key_position_in_csv", optional=False, grouping="3",
        description="Indicate the position of the key in the csv table"),

)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
print(script_params)

#set the namespace which will allow to retrieve the map annotations generated by the script
tags_namespace = "kvpairs.from.tags.script"
voc_namespace = "kvpairs.from.vocabulary.script"

# get the 'IDs' parameter of the csv file imported as annotation
key_position = script_params["Key_position_in_csv"]  #this has been added to give the user the opportunity to define the position of the key in the csv file
file_id = script_params["File_Annotation"]
file_ann = conn.getObject("FileAnnotation", file_id)
csv_text = "".join(list(file_ann.getFileInChunks()))
print("####csv content: "+str(csv_text))
lines = csv_text.split("\n")

#consider that the csv file has got headers
col_names = lines[0].split(",")
key_index = key_position   #it was 2

#creating the vocabulary
key_rows = {}

for l in lines[1:]:
    cols = l.split(",")
    if len(cols) < 2:
        continue
    key = cols[key_index].strip()  #the strip function allows to avoid the blank spaces that may be in the key names
    #handle files with multiple rows with the same name key index
    if key in key_rows:
        values = key_rows[key]
    else:
        values = []
    values.append(cols)
    key_rows[key] = values

    #in the previous script i had
    #key_rows[key] = cols   #which allowed me to get all the columns in the csv file
    #if i want to specify which columns to bring into the map annotation i should run the code below
    #key_rows[key] = [cols[0], cols[1], cols[2]]
print(key_rows.keys())

#Run the script from a project and look at all the elements within it. I can also attach the script to a single dataset or image and thanks
#to the loop below i should be able to get the action i required
# get the 'IDs' parameter (which we have restricted to 'Image' IDs)
ids = script_params["IDs"]
data_type = script_params["Data_Type"]
objects = conn.getObjects(data_type, ids)

#crete the list of annotation for the image
images = []

#loop for looking at data in project/datasets and images
if data_type == 'Project':
    for p in objects:
        for ds in p.listChildren():
            images.extend(list(ds.listChildren()))
elif data_type == 'Dataset':
    for ds in objects:
        images.extend(list(ds.listChildren()))
    if not images:
        print("No image found in dataset(s)")
else:
    images = objects

#loop to take the annotation in the keyvalue pairs already existent
for i in images:
    owner = i.getOwner().getName() #this line has been introduced to allow sysadmin to copy kvpairs on behalf of the owner's image
    print(i.name)
    ann = i.getAnnotation(tags_namespace)
    print("###annotation: "+str(ann))
    if not ann:
        continue
    #create the list of annotation to be deleted everytime that the script is run
    to_delete = [a.id for a in i.listAnnotations(ns=voc_namespace)]

    #create the list of values to be added as annotation in the KV pairs section
    new_values = []
    # get values from the kvpair section
    kvpairs = ann.getValue()

    for kv in kvpairs:
        key = kv[1].strip()  #strip again to avoid that "hidden" spaces in the key name do not return the key
        print(key)
        # logic statement: if key value matches with the value in the csv file
        if key in key_rows:
            values = key_rows[key]
            for v in values:
                #create the list with the matching values
                for col_name, value in zip(col_names, v):
                    new_values.append([col_name, value])
        else:
            print("key not found: "+str(key))


    if len(new_values) == 0:
        print("didn't find any match in the csv file")
        continue

    # Return some value(s)
    suconn = conn.suConn(owner)  #this line has been introduced to allow sysadmin to copy kvpairs on behalf of the owner's image
    map_ann = omero.gateway.MapAnnotationWrapper(suconn)
    map_ann.setNs(voc_namespace)
    map_ann.setValue(new_values)
    map_ann.save()
    i.linkAnnotation(map_ann)
    suconn.close()    #this line is necessary to "close" also the connection as "other user" as the sysadmin is now concluding to operate on behalf of the owner of the image


    #delete the previous vkpairs section
    #conn.deleteObjects('Annotation', to_delete)
    if len(to_delete) > 0:
        conn.deleteObjects('Annotation', to_delete)


# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
