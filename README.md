# kibana-dashboards-extract

Python script to export Kibana dashboards

## Usage
### Directly pass the arguments
```commandline
python3 kibana_extract.py --url http://localhost:5601 -u elastic_user -p changeme -d ./extracts
```

* required arguments
```commandline
  --url URL             Kibana URL. E.g. http://localhost:5601.
  -u USER, --user USER  Kibana user
  -p PWD, --pwd PWD     User password
```
optional arguments
```commandline
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Output directory. Default "./extracts"
```
### Use pipeline.conf file
Add parameters to **pipeline.conf** file and run **start_with_configs.py**
```editorconfig
[elastic]
host = localhost
port = 5601
user = elastic
password = changeme
```

## Dependencies
```commandline
pip install requests ndjson python_json_logger
```

## Credentials
Based on a post at [discuss.elastic.co](https://discuss.elastic.co/t/automatic-dashboard-export-from-command-line-using-python/234076) 
