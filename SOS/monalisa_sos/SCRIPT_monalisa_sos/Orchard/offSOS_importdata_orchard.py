from multiprocessing import Process as Process
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


def multiprocess(core):
    import xml.etree.ElementTree as ET
    import numpy as np

    data_folder = 'C:/monalisa_sos/DATA_monalisa_sos/Orchard/'
    # data_folder = 'Y:/ProjectData/MONALISA/MONALISA_DB/ORCHARD/EURAC_GS_L0_P/'
    template_folder = 'C:/monalisa_sos/Templates/Orchard/Templates/'
    headers = {'method': 'POST', 'Content-Type': 'application/xml', 'accept': 'application/xml'}

    url = 'http://10.8.244.39:8080/sos_test1/service'

    stations = os.listdir(data_folder)

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

    def write_and_post_xml_STM(template_folder, values, dates, dir, position, sensors, start_index, end_index):
        global x_STM
        import xml.etree.ElementTree as ET
        import datetime
        import urllib.request as re

        template = template_folder + 'Orchard_InsertObservation_Soil_Temperature_Matrix.xml'
        print(template)

        for x_STM in range(start_index, end_index):
            date_str = str(dates[x_STM])
            date = datetime.datetime(year=int(date_str[8:12]), month=int(date_str[5:7]), day=int(date_str[2:4]),
                                     hour=int(date_str[13:15]), minute=int(date_str[16:18]))

            date = str(date)

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date[0:10]) + 'T' + str(date[11:])
                elif element.text == '1':
                    element.text = str(values[x_STM, 6])
                elif element.text == '2':
                    element.text = str(values[x_STM, 8])
                elif element.text == '3':
                    element.text = str(values[x_STM, 10])
                elif element.text == 'offering':
                    element.text = 'ST_' + dir.split('/')[4] + '_matrix'
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
                'C:/monalisa_sos/Insert_observation_xml/Orchard/Insert_Observation_Orchards_STM_' + dir.split('/')[4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Orchard/Insert_Observation_Orchards_STM_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_STM, date_str, dir)

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

    def write_and_post_xml_SWP(template_folder, values, dates, dir, position, sensors, start_index, end_index):
        global x_SWP
        import xml.etree.ElementTree as ET
        import datetime
        import urllib.request as re

        template = template_folder + 'Orchard_InsertObservation_Soil_Water_Potential.xml'
        print(template)

        for x_SWP in range(start_index, end_index):
            date_str = str(dates[x_SWP])
            date = datetime.datetime(year=int(date_str[8:12]), month=int(date_str[5:7]), day=int(date_str[2:4]),
                                     hour=int(date_str[13:15]), minute=int(date_str[16:18]))

            date = str(date)

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date[0:10]) + 'T' + str(date[11:])
                elif element.text == '1':
                    element.text = str(values[x_SWP, 5])
                elif element.text == '2':
                    element.text = str(values[x_SWP, 7])
                elif element.text == '3':
                    element.text = str(values[x_SWP, 9])
                elif element.text == 'offering':
                    element.text = 'SWP_' + dir.split('/')[4]
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
                'C:/monalisa_sos/Insert_observation_xml/Orchard/Insert_Observation_Orchards_SWP_' + dir.split('/')[4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Orchard/Insert_Observation_Orchards_SWP_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_SWP, date_str, dir)

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

    def write_and_post_xml_ST(template_folder, values, dates, dir, position, sensors, start_index, end_index):
        global x_ST
        import xml.etree.ElementTree as ET
        import datetime
        import urllib.request as re

        template = template_folder + 'Orchard_InsertObservation_Soil_Temperature.xml'
        print(template)

        for x_ST in range(start_index, end_index):
            date_str = str(dates[x_ST])
            date = datetime.datetime(year=int(date_str[8:12]), month=int(date_str[5:7]), day=int(date_str[2:4]),
                                     hour=int(date_str[13:15]), minute=int(date_str[16:18]))

            date = str(date)

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date[0:10]) + 'T' + str(date[11:])
                elif element.text == '1':
                    element.text = str(values[x_ST, 1])
                elif element.text == '2':
                    element.text = str(values[x_ST, 3])
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
                'C:/monalisa_sos/Insert_observation_xml/Orchard/Insert_Observation_Orchards_ST_' + dir.split('/')[4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Orchard/Insert_Observation_Orchards_ST_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_ST, date_str, dir)

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

    def write_and_post_xml_SWC(template_folder, values, dates, dir, position, sensors, start_index, end_index):
        global x_SWC
        import xml.etree.ElementTree as ET
        import datetime
        import urllib.request as re

        template = template_folder + 'Orchard_InsertObservation_Soil_Water_Content.xml'
        print(template)

        for x_SWC in range(start_index, end_index):
            date_str = str(dates[x_SWC])
            date = datetime.datetime(year=int(date_str[8:12]), month=int(date_str[5:7]), day=int(date_str[2:4]),
                                     hour=int(date_str[13:15]), minute=int(date_str[16:18]))

            date = str(date)

            tree = ET.parse(template)
            root = tree.getroot()

            tags = root.iter()

            for element in tags:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date[0:10]) + 'T' + str(date[11:])
                elif element.text == '1':
                    element.text = str(values[x_SWC, 0])
                elif element.text == '2':
                    element.text = str(values[x_SWC, 2])
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
                'C:/monalisa_sos/Insert_observation_xml/Orchard/Insert_Observation_Orchards_SWC_' + dir.split('/')[4] +
                '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            post_file = open('C:/monalisa_sos/Insert_observation_xml/Orchard/Insert_Observation_Orchards_SWC_'
                             + dir.split('/')[4] + '.xml')
            xml = post_file.read()

            xml = xml.encode()
            post_file.close()

            req = re.Request(url, xml, headers=headers)

            response = re.urlopen(req, timeout=20)

            result = response.read()

            print(x_SWC, date_str, dir)

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

    a = core
    b = core + 1

    for w in range(a, b):
        files = os.listdir(dirs[w])
        dir = dirs[w]

        print(dir.split('/')[4])

        for x in range(0, len(files)):

            file = dir + files[x]
            print(file)

            with open(file, 'r') as f:
                num_cols = len(f.readline().split(','))

            print(num_cols)

            values = np.loadtxt(file, delimiter=',', usecols=range(1, num_cols))
            dates = np.genfromtxt(file, usecols=[0], delimiter=',', dtype=str)
            dates = dates.reshape(len(dates), 1)

            stations = ['Eppanberg', 'Kaltern', 'Laimburg', 'StPaulsFeld']
            coordinates = ['46.4592420 11.2453670', '46.3895890 11.2633670', '46.3784970 11.2903240',
                           '46.4788470 11.2696410']

            for y in range(0, len(stations)):
                if dir.split('/')[4] == stations[y]:
                    position = coordinates[y]
                    continue

            sensors = ['MatrixWaterPotentialSensor_', 'SoilWaterContentReflectometer_']

            if dir.split('/')[4] == 'Laimburg':

                try:
                    write_and_post_xml_ST(template_folder, values, dates, dir, position, sensors, 0, len(values))

                except IOError:
                    bug = x_ST

                    try:
                        write_and_post_xml_ST(template_folder, values, dates, dir, position, sensors, bug - 5, len(values))

                    except IOError:
                        bug_2 = x_ST
                        write_and_post_xml_ST(template_folder, values, dates, dir, position, sensors, bug_2 - 5, len(values))

                try:
                    write_and_post_xml_SWC(template_folder, values, dates, dir, position, sensors, 0, len(values))

                except IOError:
                    bug = x_SWC

                    try:
                        write_and_post_xml_SWC(template_folder, values, dates, dir, position, sensors, bug - 5, len(values))

                    except IOError:
                        bug_2 = x_SWC
                        write_and_post_xml_SWC(template_folder, values, dates, dir, position, sensors, bug_2 - 5, len(values))

            else:

                try:
                    write_and_post_xml_STM(template_folder, values, dates, dir, position, sensors, 0, len(values))

                except IOError:
                    bug = x_STM

                    try:
                        write_and_post_xml_STM(template_folder, values, dates, dir, position, sensors, bug - 5, len(values))

                    except IOError:
                        bug_2 = x_STM
                        write_and_post_xml_STM(template_folder, values, dates, dir, position, sensors, bug_2 - 5, len(values))

                try:
                    write_and_post_xml_SWP(template_folder, values, dates, dir, position, sensors, 0, len(values))

                except IOError:
                    bug = x_SWP

                    try:
                        write_and_post_xml_SWP(template_folder, values, dates, dir, position, sensors, bug - 5, len(values))

                    except IOError:
                        bug_2 = x_SWP
                        write_and_post_xml_SWP(template_folder, values, dates, dir, position, sensors, bug_2 - 5, len(values))

                try:
                    write_and_post_xml_ST(template_folder, values, dates, dir, position, sensors, 0, len(values))

                except IOError:
                    bug = x_ST

                    try:
                        write_and_post_xml_ST(template_folder, values, dates, dir, position, sensors, bug - 5, len(values))

                    except IOError:
                        bug_2 = x_ST
                        write_and_post_xml_ST(template_folder, values, dates, dir, position, sensors, bug_2 - 5, len(values))

                try:
                    write_and_post_xml_SWC(template_folder, values, dates, dir, position, sensors, 0, len(values))

                except IOError:
                    bug = x_SWC

                    try:
                        write_and_post_xml_SWC(template_folder, values, dates, dir, position, sensors, bug - 5, len(values))

                    except IOError:
                        bug_2 = x_SWC
                        write_and_post_xml_SWC(template_folder, values, dates, dir, position, sensors, bug_2 - 5, len(values))


tic()
if __name__ == '__main__':
    tasks = []
    procs = 4
    for i in range(0, procs):
        process = Process(target=multiprocess, args=(i,))
        tasks.append(process)

    for t in tasks:
        print(t)
        t.start()

    for t in tasks:
        t.join()

toc()
