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
#import csv


# Script definition

# Script name, description and parameters are defined here.
# These parameters will be recognised by the Insight and web clients and
# populated with the currently selected Image(s)

# this script reads the image name and convert it into a tag. It works only with images.
data_types = [rstring('Image')]
client = scripts.client(
    "create_tag_from_image_name.py",
    ("Customised script for creating a tag from the image name"),
    #scripts.Long("File_Annotation"),
    # first parameter
    scripts.String(
        "Data_Type", optional=False, values=data_types, default="Image"),
    # second parameter
    scripts.List("IDs", optional=False).ofType(rlong(0)),

)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)
script_params = client.getInputs(unwrap=True)
print script_params


# get the 'IDs' parameter of the Images
ids = unwrap(client.getInput("IDs"))
images = conn.getObjects("Image", ids)

for i in images:
    image_name = i.name
    print "image name is", image_name

    tag_ann = omero.gateway.TagAnnotationWrapper(conn)
    tag_ann.setValue(image_name)
    tag_ann.save()
    i.linkAnnotation(tag_ann)  #this is fundamental for actually copying the tag!



# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))

client.closeSession()
