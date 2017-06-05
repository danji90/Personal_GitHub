#--import modules
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import math
import urllib.request as re
import datetime
import pdb

#--read excel table to python and convert to array
table = pd.read_excel('C:/monalisa_sos/DATA_monalisa_sos/LaimburgLaboratory/harvest_2014_working.xls', sheetname='Tabelle1')
matrix = table.as_matrix()

#--define server url and headers
headers = {'method': 'POST', 'Content-Type': 'application/xml', 'accept': 'application/xml'}
url = 'http://10.8.244.39:8080/sos_test2/service'
# pdb.set_trace()
#--replace all nan values in array matrix with -99
#--52°North Sos has problems with nan in element.value field
def replace_nan(matrix):
    for j in range(0,len(matrix)):
        A = matrix[j, :]
        for i in range(0, len(A)):
            if type(A[i]) is int:
                B = np.isnan(A[i])
                if B == True:
                    A[i] = -99
            elif type(A[i]) is float:
                B = np.isnan(A[i])
                if B == True:
                    A[i] = -99
replace_nan(matrix)

# --define xml-template
data = 'C:/monalisa_sos/Templates/LaimburgLaboratory/Laimburg_InsertObservation_Template.xml'

# --list prefixes
ns = {'sos': 'http://www.opengis.net/sos/2.0',
      'swes': 'http://www.opengis.net/swes/2.0',
      'swe': 'http://www.opengis.net/swe/2.0',
      'sml': 'http://www.opengis.net/sensorML/1.0.1',
      'gml': 'http://www.opengis.net/gml/3.2',
      'xlink': 'http://www.w3.org/1999/xlink',
      'om': 'http://www.opengis.net/om/2.0',
      'sams': 'http://www.opengis.net/samplingSpatial/2.0',
      'sf': 'http://www.opengis.net/sampling/2.0',
      'xs': 'http://www.w3.org/2001/XMLSchema',
      'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

# --register prefixes in order to keep them in output-file
for prefix, uri in ns.items():
    ET.register_namespace(prefix, uri)

for i in range(0, len(matrix)):
    #--define date
    date = matrix[i,7]
    #--add seconds, resulttime has to be unique for each observation
    date = date + datetime.timedelta(seconds=i)
    str_date = str(date)
    print(date)

    # --parse xml
    tree = ET.parse(data)
    root = tree.getroot()

    # --get all elements in the xml tree
    iter = root.iter()

    #--replace values
    for element in iter:
        if element.text == '00-00-00T00:00:00':
            if matrix[i,3] == 'Laimburg_longer_pruning' or 'Laimburg_shorter_pruning' or 'Schluderns' or 'Tschengels':
                element.text = '2014-09-26' + 'T' + '00:00:00'
            elif matrix[i,3] == 'Schlanders_orchard_1' or 'Schlanders_orchard_2':
                element.text = '2014-10-10' + 'T' + '00:00:00'
            elif matrix[i,3] == 'Laimburg' or 'Leifers':
                element.text == '2014-09-12' + 'T' + '00:00:00'
        elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
            element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + str(matrix[i,3])}
        elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
            element.attrib = {'{http://www.opengis.net/gml/3.2}id': str(matrix[i,3])}
        elif element.text == 'FOI':
            element.text = str(matrix[i,3])
        elif element.text == '00-00-00T00:00:01':
            element.text = str_date[0:10] + 'T' + str_date[11:]
        elif element.text == 'Lat Lon':
            if matrix[i,3] == 'Laimburg_longer_pruning' or 'Laimburg_shorter_pruning':
                element.text = '46.38026 11.287976'
            elif matrix[i,3] == 'Schlanders_orchard_1':
                element.text = '46.624344 10.76877'
            elif matrix[i,3] == 'Schlanders_orchard_2':
                element.text = '46.623226 10.779622'
            elif matrix[i,3] == 'Laimburg':
                element.text = '46.37774 11.288795'
            elif matrix[i,3] == 'Leifers':
                element.text = '46.429476 11.324698'
            elif matrix[i,3] == 'Schluderns':
                element.text = '46.657776 10.577498'
            elif matrix[i,3] == 'Tschengels':
                element.text = '46.621994 10.632095'
        elif element.text == 'shaded':
            element.text = str(matrix[i,10])
        elif element.text == 'offering':
            element.text = str(matrix[i, -1])
        elif element.text == '1':
            element.text = str(matrix[i,11])
        elif element.text == '2':
            element.text = str(matrix[i,12])
        elif element.text == '3':
            element.text = str(matrix[i,13])
        elif element.text == '4':
            element.text = str(matrix[i,14])
        elif element.text == '5':
            element.text = str(matrix[i,15])
        elif element.text == '6':
            element.text = str(matrix[i,16])
        elif element.text == '7':
            element.text = str(matrix[i,18])
        elif element.text == '8':
            element.text = str(matrix[i,20])
        elif element.text == '9':
            element.text = str(matrix[i,21])
        elif element.text == '10':
            element.text = str(matrix[i,24])

    #--write output file
    tree.write('C:/monalisa_sos/Insert_observation_xml/LaimburgLaboratory/Laimburg_POST.xml', xml_declaration = True, encoding = 'utf-8',
               method = 'xml')

    # pdb.set_trace()
    #--open written output file to post to server
    f = open('C:/monalisa_sos/Insert_observation_xml/LaimburgLaboratory/Laimburg_POST.xml', 'r')
    xml = f.read()

    #--encode it
    xml = xml.encode()
    f.close()

    #--define request
    req = re.Request(url, xml, headers=headers)

    #--post to server
    response = re.urlopen(req)

    #--server response
    result = response.read()

    print(i)
    print(result.decode())