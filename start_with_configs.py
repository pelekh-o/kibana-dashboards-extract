#!/usr/bin/env python3

import subprocess
from helpers import config_reader

COMMAND = "./kibana_extract.py"


def main():
    kibana_configs = config_reader.get_config_section('elastic', 'pipeline.conf')
    kibana_url = f'http://{kibana_configs.get("host")}:{kibana_configs.get("port")}'
    user = kibana_configs.get('user')
    password = kibana_configs.get('password')

    cmd = [COMMAND, '--url', kibana_url, '-u', user, '-p', password]
    subprocess.call(cmd)


if __name__ == "__main__":
    main()
