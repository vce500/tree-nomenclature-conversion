Tree Naming Convention Conversion Tool
This tool converts between USDA acronyms, common names, and scientific names. Conversion can take place in any directions.
As an example, a field containing the value “ACRU” can be converted to “Acer rubrum” and/or “Red maple.” This conversion can happen in any direction (e.g. “Red maple” can also be calculated back to “ACRU”).
Copy field GPS point shapefiles into a working directory or a geodatabase. Do not the modify original GPS datasets.
Notes
1.	It does not matter what your input or output fields in the attribute table are called, but they must be of “Text” type.
2.	If the “Create New Output” option is selected, a new field will be created in the attribute table. For example, if a series of acronyms needs to be converted to scientific names, the user can check this box and a “Scientific” field will be added and populated. If converting to common names, this option will add a “Common” field. If this option is checked, the  “Existing Output Field” option will be unavailable. Users cannot write to an existing field and add a new field during the same run of the tool.
3.	This tool is case insensitive. Inputs using any capitalization can be used, and the correct names will be returned. The  capitalization of the inputs will also be corrected in the attribute table.
•	“aCrU” is fine. It will be replaced in the attribute table as “ACRU”, and will properly find “Red maple” or “Acer rubrum,” depending on the desired output name format.
4.	Leading or trailing spaces will not impact functionality. They will be ignored, and the correct capitalization will be formatted in the input field. Internal spacing errors will cause errors.
•	“  ACRU  “ and “Red maple   “ are fine because the erroneous spaces at the beginning and end.
•	“AC  RU” and “Red    maple   “ will cause errors because the erroneous spaces are in the middle.
5.	If the user specifies a field to be overwritten, the tool will do this, just as Field Calculator would.
6.	Please add additional species to the CRI spreadsheet here, as needed.
•	"G:\Active\1 Forest Resources\Tree_GIS_Scripts\Tree_Name_Scripts\Script_Tree_List.csv"
Troubleshooting
1.	Refer to the Geoprocessing status window or Results pane for error messages. Common issues will be caught and reported (e.g. field already exists, .CSV file could not be found). See the section “Error Handling” below. Additional help can be found in the Help menu sidebar of the tool.
2.	If the attribute table does not appear to populate, close it and re-open it, or remove the layer and re-add it to the map. Sometimes it just needs to refresh.
3.	Field already exists error: User has elected to add a field named “EXAMPLE,” but a field named “EXAMPLE” already exists in the feature class. Two fields cannot have the same name. “EXAMPLE” and “Example” are considered the same. Capitalization is ignored for field names.
4.	File not found error: The path to the CSV where the conversion names are stored is invalid. Verify its location. It should be in the location listed above in the Notes section.
5.	Field calculates to “NOT FOUND”:
•	Check the spelling of the inputs in the attribute table. Check the CSV as well—some USDA acronym names have been modified based on species that are most common in our work areas (see section below). If your inputs are scientific or common names, check that the same name and spelling is being used in the CSV.
•	If the species does not exist in the CSV, add it in (and let Alison know) and run the tool again.
•	A Genus sp. entry will not be found, so these entries must be edited into the attribute table manually.
6.	Call Vince for additional help.
 
List of Modified USDA Acronyms:

ACSA
ACSA2 – Acer saccharinum (Silver maple)
ACSA3 – Acer saccharum (Sugar maple)

PRSE
PRSE2 – Prunus serotina (Black cherry)
PRSE3 – Prunus serrulata (Japanese cherry)

QUMA
QUMA2 – Quercus macrocarpa (Bur oak)
QUMA3 – Quercus marilandica (Blackjack oak)

QUPA
QUPA2 – Quercus palustris (Pin oak)
QUPA5 – Quercus pagoda (Cherrybark oak)

Usage
This tool is used like any other tool in ArcMap, however it currently cannot be found using the “Search” window. The location of the tool is found in the same way a shapefile or geodatabase is found—by navigating to it using the Catalog Pane within ArcMap. Double click on “TreeNameUpdate” (with the scroll icon) to open the tool’s window.
Toolbox and script tool can be found here. See side menu help within the tool window and the descriptions below for additional information.
G:\Active\1 Forest Resources\Tree_GIS_Scripts\Tree_Name_Scripts\Updated_Code_20200211\TreeScript_20200521.tbx

Parameters (Tool User Inputs)
Tree Dataset:
The tree point dataset. This can be a feature layer that is dragged in from the table of contents, or a feature class (geodatabase or shapefile) from a file path.

Input Name Format:
What is the format of the names that you are converting from?
For example, if USDA acronyms were created in the field, then the input name format would be "Acronym."

Input Field:
The name of the input field that stores all the names you want to convert from.

Output Name Format:
The naming convention that is being converted to.

Existing Output Field:
The field where the converted names will be populated. If an empty field does not exist yet, see the parameter below.

Create New Output Field:
This option adds a blank field and populates it with the results of the conversion. If the automatic option is chosen, the output field will be called "Acronym," "Scientific," or "Common," depending on the type of conversion that is taking place.

Checking the Results Window for Missing Records
Within ArcMap, click the “Geoprocessing” dropdown at the top of the window, then click “Results.” Within the Results pane, expand the most recent run of the TreeName tool, and then expand the Messages section.
The tool will report on the provided inputs (fields added, type of conversion) and list records for which no match was found.
Double clicking on the name of the tool towards the top of this window, “TreeNameUpdate,” will re-open the tool’s window with all of the previous inputs as they were.
