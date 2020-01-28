## This document wants to describe the OMERO customised scripts made for the IMS-GIS data centre in collaboration with the [Dundee OME team](https://www.openmicroscopy.org/teams/)

The scripts were thought to respond to the needs of data users in the Falklands Islands. Some of these needs are shared across a wider user community, so please have a look and improve the scripts or use them as starting point for creating new one whenever is necessary. **Please share your scripts too.**  


The scripts are divided into groups according to the main functions they do.

1. scripts operating on file names. *These scripts are for all the users.*
2. script operating on the population of key-values pairs. *These scripts can be run by both, sysadmin and users.*



### 1 Modify file names:

__*rename_replace_image_name.py*__

The script works on images only and it assume that one or more images are selected.

The scripts it allows to:


* add a prefix to the image name.
* add a postfix to the image name
* replace the old name with a new name

![](/scripts_documentation/pictures/rename_replace_py.png)

NOTE:
It is worth mentioning that the change of the file names is only visual and not real. In terms that the original file name of the imported image is NOT changed. What is changed is how the name appears in OMERO web.


__*save_image_path_name_to_csv.py*__

The script works on images only and it assume that one or more images are selected.

The script was written based on users request to select images and have a list ready for other data analyses.

The script allows to save image name and image path (before being imported to OMERO and within OMERO server) to a csv file that is meant to be saved on a local directory.


![](/scripts_documentation/pictures/save_filename_AND_path.png)


NOTE:
For opening the csv file in excel or libre office, consider that the csv file is **space delimited**. The first column is the image name, the second refers to where the image has been imported FROM, the third is the reference on OMERO server of the user who imported the image and the date of import.

![](/scripts_documentation/pictures/csv_file_path_names.png)

__*save_image_name_to_csv.py*__

This script is the simplified version of the script above as it takes ony the image name and save it to the csv file.

![](/scripts_documentation/pictures/save_image_names_only.png)

Here how it looks the csv file once opened in excel or libeoffice

![](/scripts_documentation/pictures/image_names_csv.png)

CONSIDERATION: both scripts result not only in the creation of a csv file but also in the creation of an attachment (first icon) in the figure below

![](/scripts_documentation/pictures/selected_images_saved_csvfile.png)

**The attachment is created only for first image selected** and can be found by clicking on attachment in the right handside panel

![](/scripts_documentation/pictures/annotation_from_image_names_and_paths.png)



### 2 Work with Key-Value pairs:

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

![](/scripts_documentation/pictures/before_kv_script.png)

**AFTER RUNNING THE SCRIPT**

![](/scripts_documentation/pictures/after_kv_script.png)

NOTE:
the "merge" function works in a way that at the end of each KVpairs creation, there is only one list instead of multiple lists.

__*add_metadata19115_to_kvpairs_in_dataset.py*__

The script assumes that a csv file containing a single metadata form (ISO19115) has been attached to the selected dataset and that is activated (see below).

![](/scripts_documentation/pictures/attach_metadata_csv.png)

The csv file needs to comprise of two columns: column "A" will be converted into "KEYS", while column "B" is converted into "VALUES".

![](/scripts_documentation/pictures/metadata_table_format.png)

**NOTE:**
In the csv file, the text in column "B" requires to be in one row. Text on multiple rows will not be accepted and the script will return a mistake.

The resulting csv import is displayed here below

![](/scripts_documentation/pictures/results_metadata_in_KVpairs.png)

**IMPORTANT:** the script uses a namespace which differs from the CLIENT. It means that the imported kvpairs are not editable. The reason is that the script has been originally thought for importing the metadata ISO19115 and we didn't want to merge the metadata with other kvpairs when running the merge.py script. However, by modifying the name space the users can change the behavious of the script.

__*add_kv_pairs_from_csv.py*__

The script allows adding data from a csv file to the kvpairs list which is named "kvpairs_from_csv_script".

According to where the csv is attached to, it is possible to apply the script to the single object (e.g. selected dataset or selected images) or to the nested objects (e.g. images within the selected dataset)

 ![](/scripts_documentation/pictures/kv_pairs_fromcsv.png)

 **Important** The script has also the advantage to load the kvpairs maintining the owner of the data name.


__**delete_tags_by_names.py**__

A part from kvpairs, users can decide to delete also the tag that they linked to images. It is worth mentioning that **is the link between tag(s) and image(s) to be deleted and not the tag itself**.

The script requires first to select the object(s) from which the tag links need to be removed, then to add the names of the tags to be deleted.

The script takes one or more tag names, if more than one tag name is used, they need to be separated by comma.

![](/scripts_documentation/pictures/remove_tagnames_selected.png)

### Working with tags:

Tags are a very important feature in OMERO as they help searching for images. It is strongly advised to follow the specific **workflow** described in the points below.

1. Prepare a list of common tags (e.g. place name, months names, years, species names/genus etc) and save them on a csv file. The file comprises of two columns: tag_name and description (the latter can be blank)

![](/scripts_documentation/pictures/common_tag_list_csv.png)

**Something to bear in mind:**
in a filename, space _ - . or other symbol will be considered by OMERO as a token. It means that a tag seabirds monitoring or seabirds_monitoring in reality comprises of two searchable items: "seabirds" and "monitoring"  

2. Create a project called TAG and attach the csv file to it. Activate the attachment (see figure below), and run the script
__*add_tags_from_csv.py*__

![](/scripts_documentation/pictures/common_tag_list.png)

3. if there is more than one group and the tags need to be shared across all the groups run   

 __add_tags_to_MANYgroups_from_ONEcsv.py*.__


The new added tags can be displayed by clicking on the "tags" tab

![](/scripts_documentation/pictures/tags_tab.png)

To check if the tags appear in all the groups, just change group name and list the tags by clicking in the tags tab.

**important** in order to use these script the user running the scripts needs to own the groups.

4. keep the csv files and every time new tags need to be added archive the previous csv file and attach the new one to the TAG project and re-run the scripts above. 

**Suggestion:** Get users involved in submitting their tags centrally, run the scripts above and avoid duplication of tags.
