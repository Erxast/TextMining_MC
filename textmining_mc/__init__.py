import logging
import yaml

from os import path
from peewee import Proxy

logger = logging.getLogger(__name__)
database_proxy = Proxy()  # Create a proxy for our db.


# Load configs
with open(path.join(path.dirname(__file__), "configs.yaml"), "r") as f:
    configs = yaml.load(stream=f, Loader=yaml.FullLoader)


def init_configs():
    if not configs['paths']['project']:
        configs['paths']['project'] = path.abspath(path.join(path.dirname(__file__), '..'))

    if configs['paths']['data']['root'] == 'data':
        configs['paths']['data']['root'] = path.join(path.abspath(path.join(path.dirname(path.dirname(__file__)),
                                                                            '..')),
                                                     configs['paths']['data']['root'],
                                                     '{}_data'.format(configs['project']),
                                                     )

    return configs


# Initialize project parameters
init_configs()
