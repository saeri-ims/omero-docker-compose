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
from omero.gateway import BlitzGateway
import omero.scripts as scripts

# Script definition

# Script name, description and 2 parameters are defined here.
# These parameters will be recognised by the Insight and web clients and
# populated with the currently selected Image(s)

# this script only takes Images (not Datasets etc.)
data_types = [rstring('Image')]
client = scripts.client(
    "Scripting_Service_Example_modified.py",
    ("Example script to use as a template for getting started with the"
     " scripting service."),
    # first parameter
    scripts.String(
        "Data_Type", optional=False, values=data_types, default="Image"),
    # second parameter
    scripts.List("IDs", optional=False).ofType(rlong(0)),
)
# we can now create our Blitz Gateway by wrapping the client object
conn = BlitzGateway(client_obj=client)

# get the 'IDs' parameter (which we have restricted to 'Image' IDs)
ids = unwrap(client.getInput("IDs"))
images = conn.getObjects("Image", ids)

with open("selected_images.txt", "w") as f:
    for i in images:
    	print i.name
        image_paths = i.getImportedImageFilePaths()
        f.write(i.name)
        f.write(" ")
        f.write(", ".join(image_paths['client_paths']))
        f.write(" ")
        f.write(", ".join(image_paths['server_paths']))
        f.write('\n')


file_ann = conn.createFileAnnfromLocalFile("selected_images.txt", mimetype="text/plain", ns="image.names.foo")
image = conn.getObject("Image", ids[0])
image.linkAnnotation(file_ann)


# Return some value(s).

# Here, we return anything useful the script has produced.
# NB: The Insight and web clients will display the "Message" output.

msg = "Script ran OK"
client.setOutput("Message", rstring(msg))
client.setOutput("File_Annotation", robject(file_ann._obj))

client.closeSession()
