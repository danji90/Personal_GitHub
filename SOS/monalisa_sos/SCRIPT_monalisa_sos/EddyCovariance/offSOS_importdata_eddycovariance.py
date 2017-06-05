from multiprocessing import Process
import os

data_folder = 'C:/monalisa_sos/DATA_monalisa_sos/EddyCovariance/'


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
        A = csv[m, :]
        for n in range(0, len(A)):
            if A[n] == 'NAN':
                A[n] = -99
            elif A[n] == '-9999':
                A[n] = -99


files = os.listdir(data_folder)


def f(x):
    import pandas as pd
    import xml.etree.ElementTree as ET

    template_folder = 'C:/monalisa_sos/Templates/EddyCovariance/Templates/'
    data_folder = 'C:/monalisa_sos/DATA_monalisa_sos/EddyCovariance/'

    headers = {'method': 'POST', 'Content-Type': 'application/xml', 'accept': 'application/xml'}

    url = 'http://10.8.244.39:8080/sos_test1/service'

    files = os.listdir(data_folder)

    def write_and_post_WR_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_WR
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'NetRadiometer_'
        data = template_folder + 'EddyCovariance_InsertObservation_WR_Template.xml'

        for i_WR in range(start_index, end_index):
            date_str = csv[i_WR, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_WR, 1])
                elif element.text == '2':
                    element.text = str(csv[i_WR, 2])
                elif element.text == '3':
                    element.text = str(csv[i_WR, 3])
                elif element.text == 'offering':
                    element.text = 'WR_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_WR_'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_WR_'
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

            print(i_WR, files[n])

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

    def write_and_post_PREC_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_PREC
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'Pluviometer_'
        data = template_folder + 'EddyCovariance_InsertObservation_PREC_Template.xml'

        for i_PREC in range(start_index, end_index):
            date_str = csv[i_PREC, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_PREC, 4])
                elif element.text == 'offering':
                    element.text = 'PREC_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_PREC_'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_PREC_'
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

            print(i_PREC, files[n])

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

    def write_and_post_TEMPHUM_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_TEMPHUM
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'TempHumidityProbe_'
        data = template_folder + 'EddyCovariance_InsertObservation_TEMPHUM_Template.xml'

        for i_TEMPHUM in range(start_index, end_index):
            date_str = csv[i_TEMPHUM, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_TEMPHUM, 5])
                elif element.text == '2':
                    element.text = str(csv[i_TEMPHUM, 6])
                elif element.text == 'offering':
                    element.text = 'TEMPHUM_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write(
                'C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_TEMPHUM_'
                + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_TEMPHUM_'
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

            print(i_TEMPHUM, files[n])

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

    def write_and_post_PAR_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_PAR
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'QuantumSensor_'
        data = template_folder + 'EddyCovariance_InsertObservation_PAR_Template.xml'

        for i_PAR in range(start_index, end_index):
            date_str = csv[i_PAR, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_PAR, 13])
                elif element.text == 'offering':
                    element.text = 'PAR_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_PAR_'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_PAR_'
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

            print(i_PAR, files[n])

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

    def write_and_post_SWC_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_SWC
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'SoilWaterContentReflectometer_'
        data = template_folder + 'EddyCovariance_InsertObservation_SWC_Template.xml'

        for i_SWC in range(start_index, end_index):
            date_str = csv[i_SWC, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_SWC, 8])
                elif element.text == '2':
                    element.text = str(csv[i_SWC, 9])
                elif element.text == '3':
                    element.text = str(csv[i_SWC, 10])
                elif element.text == '4':
                    element.text = str(csv[i_SWC, 11])
                elif element.text == '5':
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
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_SWC_'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_SWC_'
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

    def write_and_post_SH_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_SH
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'HeatFluxPlate_'
        data = template_folder + 'EddyCovariance_InsertObservation_SH_Template.xml'

        for i_SH in range(start_index, end_index):
            date_str = csv[i_SH, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_SH, 14])
                elif element.text == '2':
                    element.text = str(csv[i_SH, 15])
                elif element.text == 'offering':
                    element.text = 'SH_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_SH_'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_SH_'
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

            print(i_SH, files[n])

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

    def write_and_post_WIND_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_WIND
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'SonicAnemometer_'
        data = template_folder + 'EddyCovariance_InsertObservation_WIND_Template.xml'

        for i_WIND in range(start_index, end_index):
            date_str = csv[i_WIND, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_WIND, 16])
                elif element.text == '2':
                    element.text = str(csv[i_WIND, 17])
                elif element.text == '3':
                    element.text = str(csv[i_WIND, 18])
                elif element.text == '4':
                    element.text = str(csv[i_WIND, 19])
                elif element.text == '5':
                    element.text = str(csv[i_WIND, 20])
                elif element.text == 'offering':
                    element.text = 'WIND_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_WIND_'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_WIND_'
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

            print(i_WIND, files[n])

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

    def write_and_post_CO2H2O_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_CO2H2O
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'InfraredGasAnalyzer_'
        data = template_folder + 'EddyCovariance_InsertObservation_CO2H2O_Template.xml'

        for i_CO2H2O in range(start_index, end_index):
            date_str = csv[i_CO2H2O, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_CO2H2O, 21])
                elif element.text == '2':
                    element.text = str(csv[i_CO2H2O, 22])
                elif element.text == 'offering':
                    element.text = 'CO2H2O_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_CO2H2O_'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_CO2H2O_'
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

            print(i_CO2H2O, files[n])

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

    def write_and_post_EDCOV_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_EDCOV
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'CovarianceSensors_'
        data = template_folder + 'EddyCovariance_InsertObservation_EDCOV_Template.xml'

        for i_EDCOV in range(start_index, end_index):
            date_str = csv[i_EDCOV, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_EDCOV, 23])
                elif element.text == '2':
                    element.text = str(csv[i_EDCOV, 24])
                elif element.text == '3':
                    element.text = str(csv[i_EDCOV, 25])
                elif element.text == '4':
                    element.text = str(csv[i_EDCOV, 26])
                elif element.text == '5':
                    element.text = str(csv[i_EDCOV, 27])
                elif element.text == '6':
                    element.text = str(csv[i_EDCOV, 28])
                elif element.text == '7':
                    element.text = str(csv[i_EDCOV, 29])
                elif element.text == '8':
                    element.text = str(csv[i_EDCOV, 30])
                elif element.text == '9':
                    element.text = str(csv[i_EDCOV, 31])
                elif element.text == 'offering':
                    element.text = 'EDCOV_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_EDCOV_'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_EDCOV_'
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

            print(i_EDCOV, files[n])

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

    def write_and_post_NDVI_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_NDVI
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'SpectralReflectanceSensor_'
        data = template_folder + 'EddyCovariance_InsertObservation_NDVI_Template.xml'

        for i_NDVI in range(start_index, end_index):
            date_str = csv[i_NDVI, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_NDVI, 33])
                elif element.text == '2':
                    element.text = str(csv[i_NDVI, 34])
                elif element.text == '3':
                    element.text = str(csv[i_NDVI, 35])
                elif element.text == '4':
                    element.text = str(csv[i_NDVI, 36])
                elif element.text == '5':
                    element.text = str(csv[i_NDVI, 37])
                elif element.text == 'offering':
                    element.text = 'NDVI_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_NDVI_'
                       + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_NDVI_'
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

            print(i_NDVI, files[n])

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

    def write_and_post_PRI_EddyCovariance(url, headers, csv, position, station_name, start_index, end_index):
        global error, i_PRI
        import urllib.request as re
        import xml.etree.ElementTree as ET

        sensor = 'SpectralReflectanceSensor_'
        data = template_folder + 'EddyCovariance_InsertObservation_PRI_Template.xml'

        for i_PRI in range(start_index, end_index):
            date_str = csv[i_PRI, 0]

            tree = ET.parse(data)
            root = tree.getroot()

            iter = root.iter()

            for element in iter:
                if element.text == '00-00-00T00:00:00':
                    element.text = str(date_str[0:10]) + 'T' + str(date_str[11:])
                elif element.text == '1':
                    element.text = str(csv[i_PRI, 38])
                elif element.text == '2':
                    element.text = str(csv[i_PRI, 39])
                elif element.text == '3':
                    element.text = str(csv[i_PRI, 40])
                elif element.text == '4':
                    element.text = str(csv[i_PRI, 41])
                elif element.text == '5':
                    element.text = str(csv[i_PRI, 42])
                elif element.text == 'offering':
                    element.text = 'PRI_' + station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': '#FOI'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': '#' + station_name}
                elif element.attrib == {'{http://www.opengis.net/gml/3.2}id': 'FOI'}:
                    element.attrib = {'{http://www.opengis.net/gml/3.2}id': station_name}
                elif element.text == 'FOI':
                    element.text = station_name
                elif element.attrib == {'{http://www.w3.org/1999/xlink}href': 'procedure'}:
                    element.attrib = {'{http://www.w3.org/1999/xlink}href': sensor + station_name}
                elif element.text == 'Lat Lon':
                    element.text = position

            tree.write(
                'C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_PRI_'
                + station_name + '.xml', xml_declaration=True, encoding='utf-8', method='xml')

            # --open written output file to post to server
            f = open('C:/monalisa_sos/Insert_observation_xml/EddyCovariance/Insert_Observation_EddyCovariance_PRI_'
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

            print(i_PRI, files[n])

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

    y = [0, 1, 2]

    a = 0
    b = 1

    if x > 0:
        a = b * y[x]
        b = a + 1

    if x == 2:
        b = len(files)

    print(a, b)

    for n in range(a, b):
        path_name = data_folder + files[n]
        csv = pd.read_csv(path_name, header=3)
        csv = csv.as_matrix()

        replace_none(csv)
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

        stations = ['KalternEddyCov']

        coordinates = ['46.354752 11.275313']

        for x in range(0, len(stations)):
            if station_name == stations[x]:
                position = coordinates[x]
                print(station_name, position)

        if "2015" not in files[n]:
            write_and_post_WR_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_PREC_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_TEMPHUM_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_PAR_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_SWC_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_SH_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_WIND_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_CO2H2O_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_EDCOV_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)

        # Only EC_KalternEddyCov_2015.csv has columns/values for the NDVI and PRI

        else:
            write_and_post_WR_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_PREC_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_TEMPHUM_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_PAR_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_SWC_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_SH_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_WIND_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_CO2H2O_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_EDCOV_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_NDVI_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)
            write_and_post_PRI_EddyCovariance(url, headers, csv, position, station_name, 0, csv_len)


tic()

if __name__ == '__main__':
    tasks = []
    procs = 3
    for i in range(0, procs):
        process = Process(target=f, args=(i,))
        tasks.append(process)

    for t in tasks:
        print(t)
        t.start()

    for t in tasks:
        t.join()

toc()
