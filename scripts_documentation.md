## This document wants to describe the OMERO customised scripts made for the IMS-GIS data centre in collaboration with the [Dundee OME team](https://www.openmicroscopy.org/teams/)

The scripts were thought to respond to the needs of data users in the Falklands Islands. Some of these needs are shared across a wider user community, so please have a look and improve the scripts or use them as starting point for creating new one whenever is necessary. **Please share your scripts too.**  


The scripts are divided into groups according to the main functions they do.

1. scripts operating on file names. *These scripts are for all the users.*
2. script operating on the population of key-values pairs. *These scripts can be run by both, sysadmin and users.*
3. scripts operating on tags. *These scripts are for sysadmin only.*


### Modifying file names:

__*rename_replace_image_name.py*__

The script works on images only and it assume that one or more images are selected.

The scripts it allows to:


* add a prefix to the image name.
* add a postfix to the image name
* replace the old name with a new name

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/rename_replace_py.png)

NOTE:
It is worth mentioning that the change of the file names is only visual and not real. In terms that the original file name of the imported image is NOT changed. What is changed is how the name appears in OMERO web.


__*save_image_path_name_to_csv.py*__

The script works on images only and it assume that one or more images are selected.

The script was written based on users request to select images and have a list ready for other data analyses.

The script allows to save image name and image path (before being imported to OMERO and within OMERO server) to a csv file that is meant to be saved on a local directory.


![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/save_filename_AND_path.png)


NOTE:
For opening the csv file in excel or libre office, consider that the csv file is **space delimited**. The first column is the image name, the second refers to where the image has been imported FROM, the third is the reference on OMERO server of the user who imported the image and the date of import.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/csv_file_path_names.png)

__*save_image_name_to_csv.py*__

This script is the simplified version of the script above as it takes ony the image name and save it to the csv file.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/save_image_names_only.png)

Here how it looks the csv file once opened in excel or libeoffice

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/image_names_csv.png)

CONSIDERATION: both scripts result not only in the creation of a csv file but also in the creation of an attachment (first icon) in the figure below

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/selected_images_saved_csvfile.png)

**The attachment is created only for first image selected** and can be found by clicking on attachment in the right handside panel

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/annotation_from_image_names_and_paths.png)



### Working with Key-Value pairs:

A set of scripts have been written to deal with the creation of Key-Value pairs (KVpairs). Based on inputs from the users we identified several situations:

* adding two KVpairs to a dataset from manual entry
* adding KVpairs to a dataset from csv
* adding two KVpairs to an image from manual entry
* adding a list of KVpairs to an image from manual entry
* adding KVpairs to an image from csv
* delete KVpairs from a dataset and image (TBW)
* export KVpairs from an image to csv file (TBW)

__*add 2 keys and values to a dataset and merge.py*__

The script works on dataset only (there is one script specific to images called *add 2 keys and values to an image and merge.py* and it assumes that one or more datasets are selected.

The script allows to input two key and values to the selected dataset(s). If there are already KVpairs, the new additions will be merged into one KVpairs list. See the before and after images below.

**BEFORE RUNNING THE SCRIPT**

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/before_kv_script.png)

**AFTER RUNNING THE SCRIPT**

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/after_kv_script.png)

NOTE:
the "merge" function works in a way that at the end of each KVpairs creation, there is only one list instead of multiple lists.

__*add key and values to a dataset from csv.py*__

The script assumes that a csv file has been attached to the selected dataset and that is activated (see below).

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/attach_metadata_csv.png)

The csv file needs to comprise of two columns: column "A" will be converted into "KEYS", while column "B" is converted into "VALUES".

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/metadata_table_format.png)

NOTE:
the text in column "B" requires to be in one row. Text on multiple rows will not be accepted and the script will return a mistake.

The resulting csv import is displayed here below

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/results_metadata_in_KVpairs.png)

**IMPORTANT: if the script add 2 keys and values to a dataset and merge.py is run again, all the KVpairs will be merged together. IS THERE A WAY TO AVOID IT?**

__*remove key and values from a dataset and image.py*__

The script allows the users to delete the KVpairs that have been created for images and datasets.

The script takes both, images and datasets which need to be selected before running the script.

THIS SCRIPT NEEDS TO BE WRITTEN

__*export key and values from a dataset and image to a csv file.py*__

The script allows the users to export the KVpairs from images and datasets to a csv file.

The script takes both, images and datasets which need to be selected before running the script.

THIS SCRIPT NEEDS TO BE WRITTEN

### Working with tags:

Tags are a very important feature in OMERO as they help searching for images. The IMS-GIS data centre opted to have a controlled tag system instead of a random one, based on people adding their own tags. The reasons for supporting a controlled tag system are:
* it will avoid tag repetition
* it will avoid misspelling in tags
* it should help to avoid the tags to go “wild” and instead provide some structure

The scripts dealing with tags,due to their complexity and impact on the image catalogue, are run **only by the sysadmin**.

The main concepts are:

* the sysadmin is the owner of all the tags
* tags are specific to groups and same tags can occur in more than one group
* there are tags that are common to all users and hence will be propagated to all groups
* there are tags specific to groups and these will be added by the sysadmin to the relevant groups
* sysadmin belongs to all the groups

Although some of the scripts can be run in isolation, it is strongly advised to follow the specific **workflow** described in the points below.

1. Sysadim prepares a list of common tags (e.g. place name, months names, years, species names/genus etc). The file comprises of two columns: tag_name and description
(the latter can be blank)

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/common_tag_list_csv.png)


2. Sysadim attach the csv file in the TAG project created in his/her own admin group. Activate the attachment (see figure below), and run the script *add_tags_to_MANYgroups_from_ONEcsv.py*.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/common_tag_list.png)

The new added tags can be displayed by clicking on the "tags" tab

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/tags_tab.png)

To check if the tags appear in all the groups, just change group name and list the tags by clicking in the tags tab.

**NOTE: if the tags to be added are specific to one group then:**

    2a. Sysadmin will create a project called TAG in the specific group

    2b. Sysadmin will attach the csv file to this project and activate it

    2c. Sysadmin will run the script *add_tags_from_csv.py*


3. The likelihood that a user add a tag because the tag is not in the list is very high. Hence the script *check_tag_ownership.py* is run every night to detect new tags that do not belong to the sysadmin. The result of the script is a csv file in which collects tag_name, tag_id and tag_owner.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/check_tag_ownership.png)


The file is then saved in the local directory by the sysadmin and once opened it looks like this:

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/tags_tobe_checked_csv.png)

The sysadmin can understand who are the tag owners by looking at the user name table (click on the admin tab)

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/users_list.png)


4. Sysadmin reads the csv file and make changes to the tag names (if necessary, e.g. there is a typo) and add a new column to the csv file called new_tag_name. The csv file is then attached to the project TAG within the admin group.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/admin_group_attachment_list.png)

The tags_changed_owners-DATE.csv needs to be activated.

5. Sysadmin runs the script *change_tag_ownership.py* which takes the csv file corrected by sysadmin and makes the necessary changes to both tag names and tag owner. The result of the script is that all the tags will belong to sysadmin.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/change_ownership.png)


6. There is a chance that by running the above script, tags can be duplicated. To overcome this problem Sysadmin needs to run the script *merge_tags.py* which is specific to images only and *merge_tags_for_all_objects.py* which works across projects, datasets and images. [the merge scripts require further tests]
