# This Python file uses the following encoding: utf-8

import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

with open(r"G:\PUBLIC\LinT\MOD_Sandbox_Dashboard\mod_dashboard\json\partners.geojson") as f:
    data = json.load(f)


for feature in data['features']:
    color = feature['properties']['marker-color']
    name = feature['properties']['title'].replace("é".encode("utf-8"), "&eacute;").replace("É".encode("utf-8"), "&Eacute;").replace("ń".encode("utf-8"), "&nacute;").replace("ç".encode("utf-8"), "&ccedil;")
    if feature['properties']['status'] == "Mod Sandbox Partner":
        street = feature['properties']['description'][:feature['properties']['description'].find(",")]
        city_zip = feature['properties']['description'][feature['properties']['description'].find(",") + 2:]
        html = '<div><p><span style="background-color:' + color + ';color:#fff;padding:2px">' + name + '</span><br>' + street + '<br>' + city_zip + \
               '</p></div>'
    else:
        description = feature['properties']['description'].replace("é".encode("utf-8"), "&eacute;").replace("É".encode("utf-8"), "&Eacute;")
        url = feature['properties']['url']
        html = '<div><p><span style="background-color:' + color + ';color:#fff;padding:2px">' + name + '</span><br>' + \
               description + '<br><a href="' + url + '">' + url + '</a></p></div>'
    print html
