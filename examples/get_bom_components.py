#!/usr/bin/env python

import argparse
from datetime import datetime
import json
import logging
import sys
import timestring

from blackduck.HubRestApi import HubInstance

parser = argparse.ArgumentParser("Retreive BOM component info for the given project and version")
parser.add_argument("project_name")
parser.add_argument("version")

args = parser.parse_args()

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', stream=sys.stderr, level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

hub = HubInstance()

project = hub.get_project_by_name(args.project_name)

version = hub.get_version_by_name(project, args.version)

components_url = hub.get_link(version, "components")

response = hub.execute_get(components_url)
if response.status_code == 200:
    components = response.json()
    components = components.get('items', [])
    print(json.dumps(components))