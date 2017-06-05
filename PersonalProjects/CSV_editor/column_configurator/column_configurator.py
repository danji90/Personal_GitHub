##########################################
#       CSV - Column Configurator        #
# This mini script uses pandas to read   #
# comma separated input data and write   #
# comma separated output files in any    #
# desired configuration.                 #
##########################################

import pandas as pd

# input file details
file_location = "F:\CERPLAN\Backup"
file_name = "\cerplan_generaldata_19052017_corrected"
file_suffix = ".txt"

# Define input file configuration:
input_df = pd.read_csv(file_location + file_name + file_suffix , header=0, dtype=str, encoding='utf-8')

# Example: read input columns, define output columns
print(list(input_df))

output_df = input_df[['gid', 'building_code', 'building_name', 'address', 'municipality', 'typology', 'building_services',
                'construction_year', 'user_number', 'maintenance_cost', 'the_geom', 'group_user', 'renovation_year',
                'description_renovation', 'number_computers', 'ownership']]

print(list(output_df))

# Define output file configuration:

output_df.to_csv(file_location + file_name + '_new' + '.csv', index=0, quoting=0, encoding='utf-8')