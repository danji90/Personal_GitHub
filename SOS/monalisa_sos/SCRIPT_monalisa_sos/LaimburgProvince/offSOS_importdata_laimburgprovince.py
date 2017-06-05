from multiprocessing import Process


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


# --define destination folder where textfiles are stored
data_folder = 'C:/monalisa_sos/DATA_monalisa_sos/LaimburgProvince/Laimburg_single_parameters/'

# --define xml-template folder
template_folder = 'C:/monalisa_sos/Templates/LaimburgProvince/template_single_parameters/'

# --define server url and headers
headers = {'method': 'POST', 'Content-Type': 'application/xml', 'accept': 'application/xml'}
url = 'http://10.8.244.39:8080/sos_test2/service'


def multi(x):
    import os
    text_files = os.listdir(data_folder)

    text_files_len = len(text_files)

    # --function Insert_Observation_Meteo_BZ inserts meteorological data sets to SOS-database
    def Insert_Observation_Meteo_BZ(data_folder, template_folder):
        # --import xml.etree module for xml-parsing
        import xml.etree.ElementTree as ET
        import numpy as np
        import pdb
        import os

        # --list all available text files and templates

        text_files = os.listdir(data_folder)
        xml_templates = os.listdir(template_folder)

        # --the following code snippet is used for multiprocess parallel processing

        y = [0, 1, 2, 3, 4]

        a = 0
        b = 4

        if x > 0:
            a = b * y[x]
            b = a + 4

        if x == 4:
            b = text_files_len

        print(a, b)

        # --loop through the files

        for j in range(a, b):

            path_name = data_folder + text_files[j]

            # --load .txt file to python with numpy.loadtxt
            data_set = np.loadtxt(path_name, skiprows=13)

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

            # --get observed parameter from text file
            base = os.path.basename(path_name)
            xml_id = os.path.splitext(base)[0]

            # --define xml-template, check for file names
            xml_templates_len = len(xml_templates)
            for k in range(0, xml_templates_len):
                if xml_id in xml_templates[k]:
                    data = template_folder + xml_templates[k]

            # pdb.set_trace()

            data_set_len = len(data_set)

            error = ''

            def write_and_post_xml(url, headers, data_set, data, start_index, end_index):
                global error, i
                import urllib.request as re
                import xml.etree.ElementTree as ET
                import datetime

                for i in range(start_index, end_index):
                    date_str = str(int(data_set[i, 0]))
                    date = datetime.datetime(year=int(date_str[0:4]), month=int(date_str[4:6]), day=int(date_str[6:8]),
                                             hour=int(date_str[8:10]), minute=int(date_str[10:12]),
                                             second=int(date_str[12:14]))

                    date = str(date)

                    # --parse xml
                    tree = ET.parse(data)
                    root = tree.getroot()

                    # --get all elements in the xml tree
                    iter = root.iter()

                    # -- replace values
                    for element in iter:
                        if element.text == '00-00-00T00:00:00':
                            element.text = str(date[0:10]) + 'T' + str(date[11:])
                        elif element.text == '1':
                            element.text = str(data_set[i, 1])

                    tree.write(
                        'C:/monalisa_sos/Insert_observation_xml/LaimburgProvince/Insert_Observation_Meteo_Bz.xml',
                        xml_declaration=True,
                        encoding='utf-8', method='xml')

                    # --open written output file to post to server
                    f = open('C:/monalisa_sos/Insert_observation_xml/LaimburgProvince/Insert_Observation_Meteo_Bz.xml',
                             'r')
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

                    print()
                    print(i, text_files[j])

                    server_response = ET.fromstring(result.decode())
                    server_iter = server_response.iter()
                    # print(server_response.getchildren())
                    # pdb.set_trace()

                    if not server_response.getchildren():
                        print(result.decode())
                        continue
                    else:
                        for element in server_iter:
                            error = element.text
                        if 'Observation with same values already contained in database' in error:
                            print('Observation already contained in database!')
                            continue

            try:
                write_and_post_xml(url, headers, data_set, data, 0, data_set_len)

            except IOError:
                bug = i
                pdb.set_trace()

                try:
                    write_and_post_xml(url, headers, data_set, data, bug - 5, data_set_len)

                except IOError:
                    bug_2 = i
                    write_and_post_xml(url, headers, data_set, data, bug_2 - 5, data_set_len)

    Insert_Observation_Meteo_BZ(data_folder, template_folder)

tic()

if __name__ == '__main__':
    tasks = []
    procs = 5
    for i in range(0, procs):
        process = Process(target=multi, args=(i,))
        tasks.append(process)

    for t in tasks:
        print(t)
        t.start()

    for t in tasks:
        t.join()

toc()
