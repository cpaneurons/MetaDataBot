import logging.config
import yaml


logger = logging.getLogger('__main__')
with open('log/config.yml', 'r') as obj:
    logging.config.dictConfig(yaml.safe_load(obj))