from multiprocessing import Process
import os

data_folder = 'C:/monalisa_sos/DATA_monalisa_sos/Beratungsring/'


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


def replace_none(csv):
    for m in range(0, len(csv)):
        a = csv[m, :]
        for n in range(0, len(a)):
            if a[n] == 'None':
                a[n] = -99

files = os.listdir(data_folder)


def f(x):
    import pandas as pd
    import xml.etree.ElementTree as ET

    template_folder = 'C:/monalisa_sos/Templates/Beratungsring/Templates/'
    data_folder = 'C:/monalisa_sos/DATA_monalisa_sos/Beratungsring/'

    headers = {'method': 'POST', 'Content-Type': 'application/xml', 'accept': 'application/xml'}

    url = 'http://10.8.244.39:8080/sos_test1/service'

    files = os.listdir(data_folder)

    def write_and_post_Meteo_Beratungsring(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_Meteo
        import urllib.request as re
        import xml.etree.ElementTree as ET

        pre_station = 'MeteoSensors_'
        data = template_folder + 'Beratungsring_InsertObservation_Meteo_Template.xml'

        for i_Meteo in range(start_index, end_index):
            date_str = csv[i_Meteo, 1]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_Meteo, 2])
                elif element.text == '2':
                    element.text = str(csv[i_Meteo, 3])
                elif element.text == '3':
                    element.text = str(csv[i_Meteo, 4])
                elif element.text == '4':
                    element.text = str(csv[i_Meteo, 6])
                elif element.text == '5':
                    element.text = str(csv[i_Meteo, 7])
                elif element.text == '6':
                    element.text = str(csv[i_Meteo, 10])
                elif element.text == 'offering':
                    element.text = 'Meteo_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': pre_station + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/Beratungsring/Insert_Observation_Beratungsring_Meteo'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/Beratungsring/Insert_Observation_Beratungsring_Meteo'
                     + station_name + '.xml', 'r')
            xml = f.read()

            # --encode it
            xml = xml.encode()
            f.close()
            f.close()

            # --define request
            req = re.Request(url, xml, headers=headers)

            # --post to server
            response = re.urlopen(req, timeout=20)

            # --server response
            result = response.read()

            print(i_Meteo, files[n])

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

    def write_and_post_ST_Beratungsring(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_ST
        import urllib.request as re
        import xml.etree.ElementTree as ET

        pre_station = 'SoilWaterContentReflectometer_'
        data = template_folder + 'Beratungsring_InsertObservation_ST_Template.xml'

        for i_ST in range(start_index, end_index):
            date_str = csv[i_ST, 1]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_ST, 13])
                elif element.text == '2':
                    element.text = str(csv[i_ST, 14])
                elif element.text == 'offering':
                    element.text = 'ST_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': pre_station + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/Beratungsring/Insert_Observation_Beratungsring_ST'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/Beratungsring/Insert_Observation_Beratungsring_ST'
                     + station_name + '.xml', 'r')
            xml = f.read()

            # --encode it
            xml = xml.encode()
            f.close()

            # --define request
            req = re.Request(url, xml, headers=headers)

            # --post to server
            response = re.urlopen(req, timeout=20)

            # --server response
            result = response.read()

            print(i_ST, files[n])

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

    def write_and_post_SWC_Beratungsring(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_SWC
        import urllib.request as re
        import xml.etree.ElementTree as ET

        pre_station = 'SoilWaterContentReflectometer_'
        data = template_folder + 'Beratungsring_InsertObservation_SWC_Template.xml'

        for i_SWC in range(start_index, end_index):
            date_str = csv[i_SWC, 1]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_SWC, 11])
                elif element.text == '2':
                    element.text = str(csv[i_SWC, 12])
                elif element.text == 'offering':
                    element.text = 'SWC_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': pre_station + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/Beratungsring/Insert_Observation_Beratungsring_SWC'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/Beratungsring/Insert_Observation_Beratungsring_SWC'
                     + station_name + '.xml', 'r')
            xml = f.read()

            # --encode it
            xml = xml.encode()
            f.close()

            # --define request
            req = re.Request(url, xml, headers=headers)

            # --post to server
            response = re.urlopen(req, timeout=20)

            # --server response
            result = response.read()

            print(i_SWC, files[n])

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

    y = [0, 1, 2, 3, 4]

    a = 0
    b = 2

    if x > 0:
        a = b * y[x]
        b = a + 2

    if x == 1:
        b = len(files)

    print(a, b)

    for n in range(a, b):
        path_name = data_folder + files[n]
        csv = pd.read_csv(path_name, header=1)
        csv = csv.as_matrix()

        print("Before: ")
        print(csv)

        replace_none(csv)

        print("After: ")
        print(csv)

        print(files[n])

        station_name = files[n].split('_')[1]

        print(station_name)

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

        csv_len = len(csv)

        error = ''

        stations = ['Tramin13er', 'Unterrain2FuchsangerEppan', 'Gries2NeufeldGreifensteinerweg',
                    'Girlan1Lamm', 'Lana6', 'NeumarktStiermoos',
                    'Terlan3', 'Nals2OberauCarli',
                    'Algund2', 'Terlan3a']

        coordinates = ['46.3291770 11.2445070', '46.5016200 11.2504780', '46.5017570 11.2802830',
                       '46.4558950 11.2795330', '46.6165530 11.1517880', '46.3047040 11.2627950',
                       '46.5410540 11.2285430', '46.5601320 11.2057040',
                       '46.6857810 11.1238730', '46.5409830 11.2286150']

        for x in range(0, len(stations)):
            if station_name == stations[x]:
                position = coordinates[x]
                print(station_name, position)

        try:
            write_and_post_Meteo_Beratungsring(url, headers, csv, position, station_name, 0, csv_len)

        except IOError:
            bug = i_Meteo

            try:
                write_and_post_Meteo_Beratungsring(url, headers, csv, position, station_name, bug - 5, csv_len)

            except IOError:
                bug_2 = i_Meteo
                write_and_post_Meteo_Beratungsring(url, headers, csv, position, station_name, bug_2 - 5, csv_len)

        try:
            write_and_post_ST_Beratungsring(url, headers, csv, position, station_name, 0, csv_len)

        except IOError:
            bug = i_ST

            try:
                write_and_post_ST_Beratungsring(url, headers, csv, position, station_name, bug - 5, csv_len)

            except IOError:
                bug_2 = i_ST
                write_and_post_ST_Beratungsring(url, headers, csv, position, station_name, bug_2 - 5, csv_len)

        try:
            write_and_post_SWC_Beratungsring(url, headers, csv, position, station_name, 0, csv_len)

        except IOError:
            bug = i_SWC

            try:
                write_and_post_SWC_Beratungsring(url, headers, csv, position, station_name, bug - 5, csv_len)

            except IOError:
                bug_2 = i_SWC
                write_and_post_SWC_Beratungsring(url, headers, csv, position, station_name, bug_2 - 5, csv_len)


tic()
if __name__ == '__main__':
    tasks = []
    procs = 5
    for i in range(0, procs):
        process = Process(target=f, args=(i,))
        tasks.append(process)

    for t in tasks:
        print(t)
        t.start()

    for t in tasks:
        t.join()

toc()
