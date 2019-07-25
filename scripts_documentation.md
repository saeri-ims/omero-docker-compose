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
* delete KVpairs from a dataset and image (done)
* export KVpairs from an image to csv file (EvanHuis)

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

**IMPORTANT:** the script uses a namespace which differs from the CLIENT. It means that the imported kvpairs are not editable. The reason is that the script has been originally thought for importing the metadata ISO19115 and we didn't want to merge the metadata with other kvpairs when running the merge.py script. However, by modifying the name space the users can change the behavious of the script.

__*remove key and values from a dataset and image.py*__

The script allows the users to delete the annotations (KVpairs mainly but tags are also possible if the namespace is known) that have been created for images and datasets by selecting the namespace and by deciding if they want to delete the annotation on the selected object or on the objects contained by the selected object (the so called children).

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/remove_annotation_bynamespace.png)


__*export key and values from images within a dataset to a csv file.py*__

The script has been taken from Even Huis's [repository](https://github.com/evenhuis/omero-user-scripts/tree/inplaceKV) and allows the users to export the KVpairs from images within datasets to a csv file.

Before running, the script requires the selection of a database (more than one is also permitted) then all the images nested in the databases will be detected and their kvpairs copied in a csv file.


![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/export_kvpairs_tocsv.png)

The csv file is attached to the selected dataset and is named using this syntax:

datasetNAME_metadata_out.csv

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/metadata_out_name.png)

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


**Something to bear in mind:**
in a filename, space _ - . or other symbol will be considered by OMERO as a token. It means that a tag seabirds monitoring or seabirds_monitoring in reality comprises of two searchable items: "seabirds" and "monitoring"  

2. Sysadim attach the csv file in the TAG project created in his/her own admin group. Activate the attachment (see figure below), and run the script __add_tags_to_MANYgroups_from_ONEcsv.py*.__

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/common_tag_list.png)

The new added tags can be displayed by clicking on the "tags" tab

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/tags_tab.png)

To check if the tags appear in all the groups, just change group name and list the tags by clicking in the tags tab.

**NOTE: if the tags to be added are specific to one group then:**

    2a. Sysadmin will create a project called TAG in the specific group

    2b. Sysadmin will attach the csv file to this project and activate it

    2c. Sysadmin will run the script __*add_tags_from_csv.py*__


3. The likelihood that a user add a tag because the tag is not in the list is very high. Hence the script __*check_tag_ownership.py*__ is run every night to detect new tags that do not belong to the sysadmin. The result of the script is a csv file in which collects tag_name, tag_id and tag_owner.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/check_tag_ownership.png)


The file is then saved in the local directory by the sysadmin and once opened it looks like this:

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/tags_tobe_checked_csv.png)

The sysadmin can understand who are the tag owners by looking at the user name table (click on the admin tab)

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/users_list.png)


4. Sysadmin reads the csv file and make changes to the tag names (if necessary, e.g. there is a typo) and add a new column to the csv file called new_tag_name. The csv file is then attached to the project TAG within the admin group.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/admin_group_attachment_list.png)

The tags_changed_owners-DATE.csv needs to be activated.

5. Sysadmin runs the script __*change_tag_ownership.py*__ which takes the csv file corrected by sysadmin and makes the necessary changes to both tag names and tag owner. The result of the script is that all the tags will belong to sysadmin.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/change_ownership.png)


6. There is a chance that by running the above script, tags can be duplicated. To overcome this problem Sysadmin needs to run the script __*merge_tags.py*__ which is specific to merging tags per images only and __*merge_tags_for_all_objects.py*__ which works across projects, datasets and images and will merge tags for all these objects.

**Note:** merging tags in reality means that we bring images linked to tags with the same name under only one tag. In our system the tags are all owned by the same person hence this "merging" operation is possible.

**Important:** The script recognises only tags that are written exactly in the same way. For instance, two tags linked to different images like

satellite imagery
satelliteImagery

will not be merged.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/not_matching_tags.png)

So, when the sysadmin reads the csv file (see point 4 in workflow) and makes the changes to the tag_names, he/she needs to be aware of all the tags already used, in order to avoid confusion.

**Important:** Since the number of tags used in OMERO is likely to grow esponentially, it is suggested that sysadmin prints out all the tags he/she owns from all the groups he/she belongs to (basically all, but avoid public group) in OMERO and keep the file handy when he/she renames the tags from other users. **[a script should be written for exporting all tags belonging to sysadmin]**

### Working with controlled vocabulary:

Controlled vocabulary is an organized list of words and phrases, or notation systems, that are used to initially tag content, and then to find it through navigation or search.

The type of controlled vocabulary we adopted for OMERO is hierachical and it goes from broader terms to narrower terms. Taxonomy is a good example that explains this hierarchy: we start with a large kingdom, e.g. Animalia and we end to the single species, e.g. Thalassarche melanoprhis.

We introduced the controlled vocabulary because it helps ensuring consistency, dealing with objects that are "hierarchical", and reducing ambiguity inherent in language where the same concept can be given different names.

Adopting a controlled vocabulary and maintaining the single tags it allows to keep the benefits from both approaches to tagging objects.

There are two scripts that run the controlled vocabulary:

1. __*copy_tags_2kvpairs_per_selected_objects.py*__

2. __*vocabulary to mapannotation.py*__


**How do the scripts work**

Sysadmin and the users will need to work out a hierarchy for the tags according to the images that the users need to add to OMERO.

The script takes csv files that have a structure similar to that one depicted below (as far as species names are concerned)

 ![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/controlled_vocabulary.png)

All the headers in the table above will be converted into keys in the KVpairs section. While the rows will be the corresponding values.

We first need to ensure that the tag is already in the KVpairs section and to do so we run the __*copy_tags_2kvpairs_per_selected_objects.py*__

This script copy the tags for the selected objects and for the children in the selected object to the KVpairs section and it uses the specific namespace **"kvpairs.from.tags.script"**. The namespace makes the KVpairs not editable but provides a hint to the users and the sysadmin about the script used for generating the KVpairs section.

The csv file we want to import acts as a look-up table where the tags in the OMERO "kvpairs.from.tags.script" is looked up and, if found, the values in the matching row are copied into OMERO KVpairs section.

After the __*copy_tags_2kvpairs_per_selected_objects.py*__ is run then it is the turn of __*vocabulary to mapannotation.py*__

**Important:** It is necessary to attach the csv file to the project and activate it.

The result is depicted below:

 ![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/vocabulary_to_mapannotation.png)

 As visible in the image above, the script uses another namespace which again will help the users to understand from which script and operation the KVpairs have been created.

 Having a controlled vocabulary will allow to retrieve all images that are falling within the broader classes in the hierarchy.

The figure below shows how to retrieve all images tagged with the species names which belong to the same family or to more families

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/search_multiple_families.png)


### Preparing data for the wider public:

A very good advantage of OMERO is that the catalogue allows sharing data not only within the same working group but also with the general public.

Data (images) that are targeted to become publicly available need to be "moved" (there is not such a copy/duplication of images in OMERO) to a public group.
Moving images means that physically the images are removed from one group and placed in another, with different level of permissions and accessibility.

Sysadmin will need to create a public group (e.g. public_domain) and make it read only. Then all the users will be made members of this group (this to allow them to move the files).This operation is performed by running the script called __*select_all_users_move_to_public_group.py*__ which makes a list of all the users and then adds them to the public group.  

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/for_admin_only.png)

**Important:** in order to move data from a group to another the users need to right click on the image/dataset/project and click on move to group

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/move_to_group.png)

A new window pops up with the request to indicate the name of the group (where to move the data to) and the dataset. **It is worth noticing that a user can only move data to a group to which he/she is member of.** At this point the user clicks on new and types the name of a new dataset. If the user is moving an entire dataset, he/she can write the same name of the dataset that he/she is moving.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/move_to_group_popup.png)

If a name is not provided, the data will be stored in the orphaned images folder.

Data in the public folder can be made available to the public either by adding a generic public user to the group (this i task of sysadmin) OR by sharing the link with the data.

![](https://github.com/saeri-ims/omero-docker-compose/blob/master/scripts_documentation/pictures/share_link_with_public_users.png)

**Reminder:** once the link is shared the user won't have more control on what happens with the link (e.g. who gets the link can re-share it without notifying this to the owner of the image).
