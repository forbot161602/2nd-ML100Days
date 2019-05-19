import os
import sys
import json
import logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

logger = logging.getLogger(__name__)

HOMEWORK_PATH = './homework'
HOMEWORK_FILE_EXTENSION = 'ipynb'


def reindex_ipynb():
    ipynb_path = find_ipynb()
    dump_ipynb(ipynb_path, index_ipynb(load_ipynb(ipynb_path)))


def find_ipynb():
    assert len(sys.argv) == 2, 'Take just one argument as ipynb file name without file extension.'
    ipynb_name = '.'.join([sys.argv[1].strip(), HOMEWORK_FILE_EXTENSION])
    ipynb_path, target_path = os.path.abspath(HOMEWORK_PATH), None
    try:
        for dir_path, dir_mames, file_names in os.walk(ipynb_path):
            for file_name in file_names:
                if file_name == ipynb_name:
                    target_path = os.path.join(ipynb_path, ipynb_name)
                    raise StopIteration('Loop end due to file found.')
    except StopIteration:
        logger.info('Ready to reindex file {}.'.format(target_path))
        return target_path
    else:
        raise RuntimeError('File `{}` is not found.'.format(ipynb_name))


def load_ipynb(ipynb_path):
    logger.info('Reading file...'.format(ipynb_path))
    with open(ipynb_path, 'r') as ipynb_file:
        return json.loads(ipynb_file.read())


def dump_ipynb(ipynb_path, ipynb_dict):
    logger.info('Writing file...'.format(ipynb_path))
    with open(ipynb_path, 'w') as ipynb_file:
        ipynb_file.write(json.dumps(ipynb_dict, sort_keys=True, indent=2))


def index_ipynb(ipynb_dict):
    logger.info('Total {} cells are found.'.format(len(ipynb_dict['cells'])))
    index_count = 0
    for cell_dict in ipynb_dict['cells']:
        if cell_dict['cell_type'] == 'code' and cell_dict['execution_count'] is not None:
            index_count += 1
            cell_dict['execution_count'] = index_count
            for output_dict in cell_dict['outputs']:
                if output_dict['output_type'] == 'execute_result':
                    output_dict['execution_count'] = index_count
            logger.info('Reindexing {}...'.format(index_count))
    return ipynb_dict


if __name__ == '__main__':
    reindex_ipynb()
