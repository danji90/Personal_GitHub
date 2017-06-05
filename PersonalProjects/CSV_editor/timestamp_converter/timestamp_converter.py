################################################
#                                              #
#          << Timestamp Converter >>           #
#                                              #
#  This script defines the original            #
#  timestamp's timezone in any CSV, TXT,DAT    #
#  input files, converts it to a timezone      #
#  of choice and writes the result into        #
#  an output file.                             #
#                                              #
#  Author: Daniel Marsh-Hunn                   #
#                                              #
################################################

import pytz
from datetime import datetime
import pandas as pd

# Define input file:
file_path = 'C:/Users/DMarshHunn/git/SOS/timestamp_converter/'
file = file_path + 'grassland_sample'

# Create dataframe from input file:
csv = pd.read_csv(file, header=None)

# Print pytz timzone library to find the timezone you need. Once the list is printed, copy the desired timezones and
# comment exit() to execute the rest of the script:
for tz in pytz.all_timezones:
    print(tz)
# exit()

# Define/Paste input and output timezone:
input_tz = pytz.timezone('CET')
output_tz = pytz.timezone('America/New_York')


def timestamp_converter(y):

    # Loop through rows and convert timestamp:
    for i in range(0, y.shape[0]):
        # Use iloc to select timestamps to define timezone, i iterates through
        # the rows and the second integer defines the timestamp column:
        x = ((y.iloc[i])[0])
        # Define given date time format:
        dt = datetime.strptime(x, '%Y-%m-%d %H:%M')
        # Set to input timezone:
        dt_in = input_tz.localize(dt)
        # Set to output timezone:
        dt_out = dt_in.astimezone(output_tz)
        # Replace timestamp column with
        x = str(dt_out)
        y.iloc[i, 0] = x

    print(y)

    # Replace potential slashes in output timezone (eg: Mexico/BajaNorte) to avoid errors when writing output file:
    output_tz_label = (str(output_tz)).replace("/","-")

    # Write modified dataframe into output file, set decimals in float_format
    y.to_csv(file + '_' + str(output_tz_label),
               header=False, index=False, float_format='%.3f')

# Call function
timestamp_converter(csv)
