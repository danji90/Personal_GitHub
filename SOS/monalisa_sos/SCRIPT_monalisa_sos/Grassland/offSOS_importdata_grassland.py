from multiprocessing import Process
import os


def tic():
    # Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()


def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print("Toc: start time not set")


def replace_NaN(x):
    import numpy as np
    x[np.isnan(x)] = -99


def multiprocess(core):
    import xml.etree.ElementTree as ET
    import numpy as np

    data_folder = 'C:/monalisa_sos/DATA_monalisa_sos/Grassland/'
    template_folder = 'C:/monalisa_sos/Templates/Grassland/Templates/'

    headers = {'method': 'POST', 'Content-Type': 'application/xml', 'accept': 'application/xml'}

    url = 'http://10.8.244.39:8080/sos_test2/service'

    data_folder_entries = os.listdir(data_folder)

    stations = []
    for r in range(0, len(data_folder_entries)):
        if os.path.isdir(data_folder + data_folder_entries[r]):
            stations.append(data_folder_entries[r])
        else:
            continue

    dirs = []
    NaN_rem = '_NaNremoved'

    for o in range(0, len(stations)):
        dirs.append(data_folder + stations[o] + '/' + stations[o] + NaN_rem + '/')

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

    def write_and_post_xml_ST_SRS(data_folder, template_folder, values, dates, dir, position, sensors, start_index,
                                  end_index):
        global x_ST_SRS
        import xml.etree.ElementTree as ET
        import urllib.request as re

        template = template_folder + 'Grassland_InsertObservation_Soil_Temperature.xml'
        print(template)

        for x_ST_SRS in range(start_index, end_index):
            date_str = str(dates[x_ST_SRS])
            date_time = str.split(date_str, " ")

            print(date_time[0], date_time[1])

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00':
                    element.text = str(date_time[0]) + 'T' + str(date_time[1])
                elif element.text == '1':
                    element.text = str(values[x_ST_SRS, 5])
                elif element.text == '2':
                    element.text = str(values[x_ST_SRS, 9])
                elif element.text == '3':
                    element.text = str(values[x_ST_SRS, 13])
                elif element.text == 'offering':
                    element.text = 'ST_' + dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + dir.split('/')[4]}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': dir.split('/')[4]}
                elif element.text == 'FOI':
                    element.text = dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensors[1] + dir.split('/')[4]}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write(
                'C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_ST_' + dir.split('/')[
                    4] + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_ST_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_ST_SRS, date_str, file)

            server_response = ET.fromstring(result.decode())
            server_iter = server_response.iter()

            if not server_response.getchildren():
                print(result.decode())
                continue
            else:
                for element in server_iter:
                    error = element.text
                    if 'Observation with same values already contained in database' in error:
                        print('Observation already contained in database!')
                        continue

    def write_and_post_xml_SWC_SRS(data_folder, template_folder, values, dates, dir, position, sensors, start_index,
                                   end_index):
        global x_SWC_SRS
        import xml.etree.ElementTree as ET
        import urllib.request as re

        template = template_folder + 'Grassland_InsertObservation_Soil_Water_Content.xml'
        print(template)

        for x_SWC_SRS in range(start_index, end_index):
            date_str = str(dates[x_SWC_SRS])

            date_time = str.split(date_str, " ")

            print(date_time[0], date_time[1])

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00':
                    element.text = str(date_time[0]) + 'T' + str(date_time[1])
                elif element.text == '1':
                    element.text = str(values[x_SWC_SRS, 3])
                elif element.text == '2':
                    element.text = str(values[x_SWC_SRS, 7])
                elif element.text == '3':
                    element.text = str(values[x_SWC_SRS, 11])
                elif element.text == 'offering':
                    element.text = 'SWC_' + dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + dir.split('/')[4]}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': dir.split('/')[4]}
                elif element.text == 'FOI':
                    element.text = dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensors[1] + dir.split('/')[4]}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write(
                'C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_SWC_' + dir.split('/')[
                    4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_SWC_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_SWC_SRS, date_str, file)

            server_response = ET.fromstring(result.decode())
            server_iter = server_response.iter()

            if not server_response.getchildren():
                print(result.decode())
                continue
            else:
                for element in server_iter:
                    error = element.text
                    if 'Observation with same values already contained in database' in error:
                        print('Observation already contained in database!')
                        continue

    def write_and_post_xml_PAR_SRS(data_folder, template_folder, values, dates, dir, position, sensors, start_index,
                                   end_index):
        global x_PAR_SRS
        import xml.etree.ElementTree as ET
        import urllib.request as re

        template = template_folder + 'Grassland_InsertObservation_Photosynthetically_Active_Radiation.xml'
        print(template)

        for x_PAR_SRS in range(start_index, end_index):
            date_str = str(dates[x_PAR_SRS])

            print("wank")
            date_time = str.split(date_str, " ")

            print(date_time[0], date_time[1])

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00':
                    element.text = str(date_time[0]) + 'T' + str(date_time[1])
                elif element.text == '1':
                    element.text = str(values[x_PAR_SRS, 15])
                elif element.text == '2':
                    element.text = str(values[x_PAR_SRS, 17])
                elif element.text == 'offering':
                    element.text = 'PAR_' + dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + dir.split('/')[4]}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': dir.split('/')[4]}
                elif element.text == 'FOI':
                    element.text = dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensors[0] + dir.split('/')[4]}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write(
                'C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_PAR_' + dir.split('/')[
                    4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_PAR_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_PAR_SRS, date_str, file)

            server_response = ET.fromstring(result.decode())
            server_iter = server_response.iter()

            if not server_response.getchildren():
                print(result.decode())
                continue
            else:
                for element in server_iter:
                    error = element.text
                    if 'Observation with same values already contained in database' in error:
                        print('Observation already contained in database!')
                        continue

    def write_and_post_xml_NDVI_SRS(data_folder, template_folder, values, dates, dir, position, sensors, start_index,
                                    end_index):
        global x_NDVI
        import xml.etree.ElementTree as ET
        import urllib.request as re

        template = template_folder + 'Grassland_InsertObservation_NDVI.xml'
        print(template)

        for x_NDVI in range(start_index, end_index):
            date_str = str(dates[x_NDVI])

            date_time = str.split(date_str, " ")

            print(date_time[0], date_time[1])

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00':
                    element.text = str(date_time[0]) + 'T' + str(date_time[1])
                elif element.text == '1':
                    element.text = str(values[x_NDVI, 19])
                elif element.text == '2':
                    element.text = str(values[x_NDVI, 21])
                elif element.text == '3':
                    element.text = str(values[x_NDVI, 23])
                elif element.text == '4':
                    element.text = str(values[x_NDVI, 25])
                elif element.text == '5':
                    element.text = str(values[x_NDVI, 27])
                elif element.text == '6':
                    element.text = str(values[x_NDVI, 28])
                elif element.text == '7':
                    element.text = str(values[x_NDVI, 29])
                elif element.text == 'offering':
                    element.text = 'NDVI_' + dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + dir.split('/')[4]}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': dir.split('/')[4]}
                elif element.text == 'FOI':
                    element.text = dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensors[2] + dir.split('/')[4]}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write(
                'C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_NDVI_' + dir.split('/')[
                    4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_NDVI_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_NDVI, date_str, file)

            server_response = ET.fromstring(result.decode())
            server_iter = server_response.iter()

            if not server_response.getchildren():
                print(result.decode())
                continue
            else:
                for element in server_iter:
                    error = element.text
                    if 'Observation with same values already contained in database' in error:
                        print('Observation already contained in database!')
                        continue

    def write_and_post_xml_PRI_SRS(data_folder, template_folder, values, dates, dir, position, sensors, start_index,
                                   end_index):
        global x_PRI
        import xml.etree.ElementTree as ET
        import urllib.request as re

        template = template_folder + 'Grassland_InsertObservation_PRI.xml'
        print(template)

        for x_PRI in range(start_index, end_index):
            date_str = str(dates[x_PRI])

            date_time = str.split(date_str, " ")

            print(date_time[0], date_time[1])

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00':
                    element.text = str(date_time[0]) + 'T' + str(date_time[1])
                elif element.text == '1':
                    element.text = str(values[x_PRI, 31])
                elif element.text == '2':
                    element.text = str(values[x_PRI, 33])
                elif element.text == '3':
                    element.text = str(values[x_PRI, 35])
                elif element.text == '4':
                    element.text = str(values[x_PRI, 37])
                elif element.text == '5':
                    element.text = str(values[x_PRI, 39])
                elif element.text == '6':
                    element.text = str(values[x_PRI, 40])
                elif element.text == '7':
                    element.text = str(values[x_PRI, 41])
                elif element.text == 'offering':
                    element.text = 'PRI_' + dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + dir.split('/')[4]}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': dir.split('/')[4]}
                elif element.text == 'FOI':
                    element.text = dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensors[2] + dir.split('/')[4]}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write(
                'C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_PRI_' + dir.split('/')[
                    4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_PRI_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_PRI, date_str, file)

            server_response = ET.fromstring(result.decode())
            server_iter = server_response.iter()

            if not server_response.getchildren():
                print(result.decode())
                continue
            else:
                for element in server_iter:
                    error = element.text
                    if 'Observation with same values already contained in database' in error:
                        print('Observation already contained in database!')
                        continue

    def write_and_post_xml_ST_STD(data_folder, template_folder, values, dates, dir, position, sensors, start_index,
                                  end_index):

        global x_ST_STD
        import xml.etree.ElementTree as ET
        import urllib.request as re

        template = template_folder + 'Grassland_InsertObservation_Soil_Temperature.xml'
        print(template)

        for x_ST_STD in range(start_index, end_index):
            date_str = str(dates[x_ST_STD])

            date_time = str.split(date_str, " ")

            print(date_time[0], date_time[1])

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00':
                    element.text = str(date_time[0]) + 'T' + str(date_time[1])
                elif element.text == '1':
                    element.text = str(values[x_ST_STD, 5])
                elif element.text == '2':
                    element.text = str(values[x_ST_STD, 9])
                elif element.text == '3':
                    element.text = str(values[x_ST_STD, 13])
                elif element.text == 'offering':
                    element.text = 'ST_' + dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + dir.split('/')[4]}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': dir.split('/')[4]}
                elif element.text == 'FOI':
                    element.text = dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensors[1] + dir.split('/')[4]}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write(
                'C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_ST_' + dir.split('/')[
                    4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_ST_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_ST_STD, date_str, file)

            server_response = ET.fromstring(result.decode())
            server_iter = server_response.iter()

            if not server_response.getchildren():
                print(result.decode())
                continue
            else:
                for element in server_iter:
                    error = element.text
                    if 'Observation with same values already contained in database' in error:
                        print('Observation already contained in database!')
                        continue

    def write_and_post_xml_SWC_STD(data_folder, template_folder, values, dates, dir, position, sensors, start_index,
                                   end_index):
        global x_SWC_STD
        import xml.etree.ElementTree as ET
        import urllib.request as re

        template = template_folder + 'Grassland_InsertObservation_Soil_Water_Content.xml'
        print(template)

        for x_SWC_STD in range(start_index, end_index):
            date_str = str(dates[x_SWC_STD])

            date_time = str.split(date_str, " ")

            print(date_time[0], date_time[1])

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00':
                    element.text = str(date_time[0]) + 'T' + str(date_time[1])
                elif element.text == '1':
                    element.text = str(values[x_SWC_STD, 3])
                elif element.text == '2':
                    element.text = str(values[x_SWC_STD, 7])
                elif element.text == '3':
                    element.text = str(values[x_SWC_STD, 11])
                elif element.text == 'offering':
                    element.text = 'SWC_' + dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + dir.split('/')[4]}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': dir.split('/')[4]}
                elif element.text == 'FOI':
                    element.text = dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensors[1] + dir.split('/')[4]}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write(
                'C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_SWC_' + dir.split('/')[
                    4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_SWC_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_SWC_STD, date_str, file)

            server_response = ET.fromstring(result.decode())
            server_iter = server_response.iter()

            if not server_response.getchildren():
                print(result.decode())
                continue
            else:
                for element in server_iter:
                    error = element.text
                    if 'Observation with same values already contained in database' in error:
                        print('Observation already contained in database!')
                        continue

    def write_and_post_xml_PAR_STD(data_folder, template_folder, values, dates, dir, position, sensors, start_index,
                                   end_index):
        global x_PAR_STD
        import xml.etree.ElementTree as ET
        import urllib.request as re

        template = template_folder + 'Grassland_InsertObservation_Photosynthetically_Active_Radiation.xml'
        print(template)

        for x_PAR_STD in range(start_index, end_index):
            date_str = str(dates[x_PAR_STD])

            date_time = str.split(date_str, " ")

            print(date_time[0], date_time[1])

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00':
                    element.text = str(date_time[0]) + 'T' + str(date_time[1])
                elif element.text == '1':
                    element.text = str(values[x_PAR_STD, 15])
                elif element.text == '2':
                    element.text = str(values[x_PAR_STD, 17])
                elif element.text == 'offering':
                    element.text = 'PAR_' + dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + dir.split('/')[4]}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': dir.split('/')[4]}
                elif element.text == 'FOI':
                    element.text = dir.split('/')[4]
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensors[0] + dir.split('/')[4]}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write(
                'C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_PAR_' + dir.split('/')[
                    4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Grassland/Insert_Observation_Grassland_PAR_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_PAR_STD, date_str, file)

            server_response = ET.fromstring(result.decode())
            server_iter = server_response.iter()

            if not server_response.getchildren():
                print(result.decode())
                continue
            else:
                for element in server_iter:
                    error = element.text
                    if 'Observation with same values already contained in database' in error:
                        print('Observation already contained in database!')
                        continue

    y = [0, 1, 2, 3, 4, 5, 6]

    a = 0
    b = 2

    if core > 0:
        a = b * y[core]
        b = a + 2

    if core == 6:
        b = len(stations)

    print(a, b)

    for w in range(a, b):
        files = os.listdir(dirs[w])
        dir = dirs[w]
        for u in range(0, len(files)):
            file = dirs[w] + files[u]

            print(dir)
            print(files)
            print(file)
            with open(file, 'r') as f:
                lines = f.readlines()
                num_cols = len(lines[0].split(','))
                dates = []
                for col in lines:
                    dates.append(col.split(',')[0])

            f.close()

            try:
                values = np.loadtxt(file, delimiter=',', usecols=range(1, num_cols))

                print(values)

                replace_NaN(values)

            except ValueError:
                continue

            len_values = len(values)

            stations = ['vimes1500', 'vimef1500', 'nepas2000',
                        'nemef2000', 'nemes2000', 'nemes1500',
                        'domes2000', 'domef2000', 'domef1500',
                        'vimes2000', 'vimef2000', 'dopas2000',
                        'nemef1500', 'domes1500', 'vipas2000']

            coordinates = ['46.6861430 10.5798810', '46.7198030 10.8618760', '46.8070610 12.2724030',
                           '46.8037190 12.2728320', '46.8053000 12.2705160', '47.0346160 12.0918570',
                           '46.5484730 11.6067010', '46.5328090 11.6309700', '46.4010020 11.4542110',
                           '46.7540930 10.7792290', '46.7451510 10.7888450', '46.3495330 11.4480640',
                           '47.0376000 12.1020230', '46.3972160 11.4464830', '46.7494720 10.7896630']

            print(dir.split('/')[4])

            for y in range(0, len(stations)):
                if dir.split('/')[4] == stations[y]:
                    position = coordinates[y]
                    print(position)
                    print()
                    continue

            sensors = ['QuantumSensor_', 'SoilWaterContentReflectometer_', 'SpectralReflectanceSensor_']

            standard_srs = ['domef1500', 'domef2000', 'nemef1500', 'nemef2000', 'vimef2000', 'vimes1500']

            if dir.split('/')[4] in standard_srs:
                write_and_post_xml_ST_SRS(data_folder, template_folder, values, dates, dir, position, sensors, 0,
                                          len_values)
                write_and_post_xml_SWC_SRS(data_folder, template_folder, values, dates, dir, position, sensors, 0,
                                           len_values)
                write_and_post_xml_PAR_SRS(data_folder, template_folder, values, dates, dir, position, sensors, 0,
                                           len_values)
                write_and_post_xml_NDVI_SRS(data_folder, template_folder, values, dates, dir, position, sensors, 0,
                                            len_values)
                write_and_post_xml_PRI_SRS(data_folder, template_folder, values, dates, dir, position, sensors, 0,
                                           len_values)

            else:
                write_and_post_xml_ST_STD(data_folder, template_folder, values, dates, dir, position, sensors, 0,
                                          len_values)
                write_and_post_xml_SWC_STD(data_folder, template_folder, values, dates, dir, position, sensors, 0,
                                           len_values)
                write_and_post_xml_PAR_STD(data_folder, template_folder, values, dates, dir, position, sensors, 0,
                                           len_values)


tic()
if __name__ == '__main__':
    tasks = []
    procs = 7
    for i in range(0, procs):
        process = Process(target=multiprocess, args=(i,))
        tasks.append(process)

    for t in tasks:
        print(t)
        t.start()

    for t in tasks:
        t.join()

toc()
