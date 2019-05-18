import os
import sys
import json
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

HOMEWORK_PATH = './homework'


def reindex_ipynb():
    ipynb_path = find_ipynb()
    dump_ipynb(ipynb_path, index_ipynb(load_ipynb(ipynb_path)))


def find_ipynb():
    assert len(sys.argv) == 2, 'Take just one argument as ipynb file name without file extension.'
    ipynb_path = os.path.abspath(HOMEWORK_PATH)
    ipynb_name = sys.argv[1].strip() + '.ipynb'
    for dir_path, dir_mames, file_names in os.walk(ipynb_path):
        for file_name in file_names:
            if file_name == ipynb_name:
                return os.path.join(ipynb_path, ipynb_name)
    raise RuntimeError('File `{}` not found.'.format(ipynb_name))


def load_ipynb(ipynb_path):
    logger.info('Read file: {}'.format(ipynb_path))
    with open(ipynb_path, 'r') as ipynb_file:
        return json.loads(ipynb_file.read())


def dump_ipynb(ipynb_path, ipynb_dict):
    logger.info('Write file: {}'.format(ipynb_path))
    with open(ipynb_path, 'w') as ipynb_file:
        ipynb_file.write(json.dumps(ipynb_dict, sort_keys=True, indent=2))


def index_ipynb(ipynb_dict):
    logger.info('Find cells: {}'.format(len(ipynb_dict['cells'])))
    index_count = 0
    cell_processible = False
    for cell_dict in ipynb_dict['cells']:
        cell_processible = cell_dict['cell_type'] == 'code' and cell_dict['execution_count'] is not None
        if cell_processible:
            index_count += 1
            cell_dict['execution_count'] = index_count
            for output_dict in cell_dict['outputs']:
                if output_dict['output_type'] == 'execute_result':
                    output_dict['execution_count'] = index_count
            logger.info('Reindex: {}'.format(index_count))
    return ipynb_dict


if __name__ == '__main__':
    reindex_ipynb()
