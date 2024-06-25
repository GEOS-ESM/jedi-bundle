import sys
from jedi_bundle.utils.logger import Logger
from jedi_bundle.utils.yaml import load_yaml

logger = Logger('Pinned Versions Test')
build_yaml_path = sys.argv[1]
build_dict = load_yaml(logger, build_yaml_path)

if 'pinned_versions' not in build_dict:
    raise Exception('Pinned versions not found in build_dict')
