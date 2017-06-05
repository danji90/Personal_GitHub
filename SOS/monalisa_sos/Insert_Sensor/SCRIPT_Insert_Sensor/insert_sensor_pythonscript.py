import os
import urllib.request as re

url = 'http://10.8.244.39:8080/sos_test2/service'

headers = {'method': 'POST', 'Content-Type': 'application/xml', 'accept': 'application/xml'}

# Comment the the datafolders you don't want, or insert your own path and folder

# data_folder = 'C:/monalisa_sos/Insert_Sensor/XMLs/Grassland/'
data_folder = 'C:/monalisa_sos/Insert_Sensor/XMLs/Beratungsring/'
# data_folder = 'C:/monalisa_sos/Insert_Sensor/XMLs/EddyCovariance/'
# data_folder = 'C:/monalisa_sos/Insert_Sensor/XMLs/LaimburgProvince/'
# data_folder = 'C:/monalisa_sos/Insert_Sensor/XMLs/EddyCovariance/'
# data_folder = 'C:/monalisa_sos/Insert_Sensor/XMLs/Orchard/'

data_folder_entries = os.listdir(data_folder)

for y in data_folder_entries:
    file = (data_folder + y)

    print(file)

    post_file = open(file)

    xml = post_file.read()

    xml = xml.encode()
    post_file.close()


    req = re.Request(url, xml, headers=headers)

    response = re.urlopen(req, timeout=20)

    result = response.read()

    print(result.decode())