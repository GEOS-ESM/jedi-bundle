import sys
from jedi_bundle.utils.logger import Logger
from jedi_bundle.utils.yaml import load_yaml

'''
    Script to search for 'pinned_versions' keyword in build.yaml
    during github action test.
'''

logger = Logger('Pinned Versions Test')
build_yaml_path = sys.argv[1]
build_dict = load_yaml(logger, build_yaml_path)

if 'pinned_versions' not in build_dict:
    raise Exception('Pinned versions not found in build_dict')
