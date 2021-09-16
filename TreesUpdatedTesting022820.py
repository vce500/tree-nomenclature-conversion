"""
Tree Name Conversion Geoprocessing Tool

This script is meant to be built into a toolbox and used within ArcGIS Pro.
It will read a feature class with a field containing acronyms, scientific names,
and/or common names, and calculate equivalent names in other formats, to new
or existing fields.

Conversion names to be used must be provided in a CSV file.

VEdwards 20201005
"""
#--------------------------------------------------------------------------------#
# IMPORTS
import arcpy as ap
import csv
import os
import sys
import traceback
#--------------------------------------------------------------------------------#
# INPUTS
tree_dataset = ap.GetParameterAsText(0)
input_format = ap.GetParameterAsText(1)
input_fld = ap.GetParameterAsText(2)
output_format = ap.GetParameterAsText(3)
output_fld = ap.GetParameterAsText(4)
create_field = ap.GetParameter(5)
mark_unfound = ap.GetParameter(6)

#csv_file_path = r"G:\Active\1 Forest Resources\Tree_GIS_Scripts\Tree_Name_Scripts\Tree_Name_Conversion_GPTool\Script_Master_Tree_List.csv"
csv_file_path = ap.GetParameterAsText(7)
#--------------------------------------------------------------------------------#
#DERIVED INPUTS
# If the user wants to specifically mark the output fields so they are easier to
#       recognize as not having had a match, use the string below.
if mark_unfound:
    UNFOUND = "*NOT FOUND*"
else:
    UNFOUND = None

oid_fldname = ap.Describe(tree_dataset).OIDFieldName
#--------------------------------------------------------------------------------#
#SETTINGS
#--------------------------------------------------------------------------------#
# FUNCTIONS
def check_csv_exists(csv_file):
    """
    Verify file path to the tree name CSV is valid; else, exit.
    """
    if os.path.exists(csv_file) == False:
        ap.AddError('\nTree .CSV file was not found...\nCheck .CSV file path...\n')
        sys.exit(1)

def build_tree_dictionary(csv_file, in_format, out_format):
    """
    Generate tree dictionary from the given CSV, and the provided mapping
    direction from the user.
    """
    column_code_dict = {'Acronym': 0, 'Scientific': 1, 'Common': 2}

    # Get the column number in the CSV that should be used as the KEY,
    #       and the column number in the CSV that should be used as the VALUE.
    in_column_num = column_code_dict[in_format]
    out_column_num = column_code_dict[out_format]

    new_tree_dict = {}

    with open(csv_file) as treefile:
        ap.AddMessage('Constructing tree name dictionary...\n')
        # Read the key in as all lowercase.
        for row in csv.reader(treefile):
            dict_key = row[in_column_num].lower()
            dict_val = row[out_column_num]

            new_tree_dict[dict_key] = dict_val

    return new_tree_dict

def format_input_field(in_fld, in_fld_type):
    """
    Reformats the input to match standard formatting of inputs:
        Acronyms: all caps
        Common/Scientific: sentence case
    Returns an updated string that will replace the input in the
    attribute table.
    """
    if in_fld_type == 'Acronym':
        update_input = in_fld.upper()
    elif in_fld_type in ['Scientific', 'Common']:
        update_input = in_fld.capitalize()
    return update_input
#--------------------------------------------------------------------------------#
# MAIN
check_csv_exists(csv_file_path)

tree_dictionary = build_tree_dictionary(csv_file_path, input_format, output_format)

# If the user has chosen to create a new field, check if that field already
#       exists. If so, the tool exits. If not, adds the field.
if create_field:
    if len(ap.ListFields(tree_dataset, wild_card=output_format)) > 0:
        ap.AddError(f'"{output_format}" field already exists.\n')
        sys.exit(1)
    else:
        ap.management.AddField(tree_dataset, output_format, "TEXT", field_length=80)
        ap.AddMessage(f'Adding {output_format} field...\n')
        # The output field will not have been provided if a new field is being added,
        #       so set the destination output to be the new field.
        output_fld = output_format

ap.AddMessage(f'Converting {input_format} to {output_format}...\n')

# Using a cursor, reads and update rows in the feature class. Using the input field
#       as the key, returns the associated value, or 'UNFOUND' variable.
# Depending on input name type, cleans up the inputs based on formatting rules.
with ap.da.UpdateCursor(tree_dataset, ["OID@", input_fld, output_fld]) as cursor:
    for row in cursor:
        try:

            ap.AddMessage(f'{row[1]}, {row[2]}')

            # Read the input as lowercase, to match the keys which are also all
            #       lowercase. Remove internal extra spaces with split/join.
            input_name = ' '.join(str(row[1]).lower().split())
            
            # From the given input, request an output from the dictionary. If none
            #       is found, .get() returns the UNFOUND value.
            output_name = tree_dictionary.get(input_name, UNFOUND)

            # If the output_name == None, meaning the UNFOUND constant variable is
            #       None and therefore the user does not want to mark unfound matches
            #       in the output fields, do not update output fields row[1] and row[2].
            #       Proceed to next row without updating using "continue".
            # elif the user has elected to use the "NOT FOUND" setting, update output
            #       field row[2] to be "NOT FOUND".
            # else, .get() returned an actual value; set output row[2] to that value.
            #       Also, update the formatting of the input value.

            if output_name is None:
                ap.AddWarning(f'No matching record for {oid_fldname} {row[0]}: "{row[1]}".')
                continue
            elif output_name == UNFOUND:
                ap.AddWarning(f'{UNFOUND} populated for {oid_fldname} {row[0]}: "{row[1]}".')
                row[2] = output_name
            else:
                row[1] = format_input_field(input_name, input_format)
                row[2] = output_name

            # Update output row with UNFOUND value, OR
            # update formatting of input AND new name in output field.
            cursor.updateRow(row)

        except Exception:
            etype, evalue, tback = sys.exc_info()
            tback_info = traceback.format_tb(tback)[0]
            err_msg = (f"Traceback Info:\n{tback_info}\n{etype.__name__}: {evalue}")
            ap.AddWarning(err_msg)
