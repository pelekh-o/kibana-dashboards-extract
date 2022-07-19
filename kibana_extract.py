#!/usr/bin/env python3

import sys
import requests
import ndjson
import os
import argparse

from helpers.logger import logger
logging = logger(__name__)

FIND_ENDPOINT = 'api/saved_objects/_find'
EXPORT_ENDPOINT = 'api/saved_objects/_export'

headers = {
    'kbn-xsrf': 'true',
    'Content-Type': 'application/json',
}
params = {
    'type': 'dashboard'
}


def extract(url, elastic_user, elastic_password, extracts_dir):
    url_space = f'{url}/api/spaces/space'

    try:
        response = requests.get(url_space, auth=(elastic_user, elastic_password))
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f'Failed to retrieve spaces from Kibana: {conn_err}')
        sys.exit(1)

    if response.status_code != 200:
        logging.error(f'Received {response.status_code} response: {response.text}')
        sys.exit(1)

    spaces_list = response.json()
    logging.info(f'Found {len(spaces_list)} spaces: {[s["name"] for s in spaces_list]}')

    for space in spaces_list:
        space_id = space.get('id')

        if space_id == 'default':
            dashboard_url = f'{url}/{FIND_ENDPOINT}'
            dashboard_export_url = f'{url}/{EXPORT_ENDPOINT}'
        else:
            dashboard_url = f'{url}/s/{space_id}/{FIND_ENDPOINT}'
            dashboard_export_url = f'{url}/s/{space_id}/{EXPORT_ENDPOINT}'

        response = requests.get(dashboard_url, params=params, headers=headers, auth=(elastic_user, elastic_password))
        if response.status_code != 200:
            logging.error(f'Received {response.status_code} response: {response.text}')
            sys.exit(1)

        objects_page = response.json()
        dashboards_list = objects_page['saved_objects']
        logging.info(f'Found {len(dashboards_list)} dashboards in space {space.get("name")}: '
                     f'{[d["attributes"].get("title") for d in dashboards_list]}')

        for dashboard in dashboards_list:
            dashboard_id = dashboard.get('id')
            dashboard_title = dashboard.get('attributes').get('title')

            data = '''
                    {
                        "objects": [
                            {
                                "type": "dashboard",
                                "id": "%s"
                            }
                        ],
                        "includeReferencesDeep": true
                    }''' % dashboard_id

            response = requests.post(dashboard_export_url, headers=headers, data=data,
                                     auth=(elastic_user, elastic_password))
            if response.status_code != 200:
                logging.error(f'Received {response.status_code} response: {response.text}')
                sys.exit(1)

            items = response.json(cls=ndjson.Decoder)
            content = ndjson.dumps(items)

            export_file = dashboard_title.lower().replace(" ", "_")
            try:
                f = open(f'{extracts_dir}/{export_file}.ndjson', 'w')
                f.write(content)
                f.close()
                logging.info(f'{dashboard_title} dashboard successfully saved to file {f.name}')
            except Exception as err:
                logging.error(f'Failed to extract dashboard {dashboard_title} to the file: {err}')


def main():
    parser = argparse.ArgumentParser(
        description='Exporting Kibana dashboards to ndjson',
        usage='python3 kibana_extract.py --url http://localhost:5601 -u elastic_user -p changeme -d ./extracts'
    )
    required = parser.add_argument_group('required arguments')
    required.add_argument('--url', help='Kibana URL. E.g. http://localhost:5601.', required=True)
    required.add_argument('-u', '--user', help='Kibana user', required=True)
    required.add_argument('-p', '--pwd', help='User password', required=True)
    parser.add_argument('-d', '--dir', help='Output directory. Default "./extracts"', required=False, default='./extracts')
    args = parser.parse_args()

    logging.info('The script has started')

    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
        logging.debug(f'Created folder {args.dir}')

    extract(args.url, args.user, args.pwd, args.dir)


if __name__ == '__main__':
    main()
