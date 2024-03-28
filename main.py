import os
import unicodedata
import logging

this_wd = '/home/jose.runin/jose.runin_nfs/ascii_rewriter'

logging.basicConfig(filename=os.path.join(this_wd, 'ascii_rewriter.log'), level=logging.INFO)


def try_encoding(data, encode):
    try:
        data.encode(encode)
        return True
    except UnicodeEncodeError:
        return False


def rewrite_files_encoding(folder_path, ends_in = '.thrift', encode = 'ascii'):
    retorno = []
    logs = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.endswith(ends_in):
                with open(file_path, 'r') as f:
                    content = f.read()
                if not try_encoding(content, encode):
                    pathfull, extension = os.path.splitext(file_path)
                    newPath = os.path.join(pathfull + '_old' + extension)
                    try:
                        logging.info('rewriting file: {}'.format(file_path))
                        os.rename(file_path, newPath)
                        with open(newPath, 'r') as f:
                            content = f.read()
                        normalized = unicodedata.normalize('NFKD', content).encode(encode, 'ignore')
                        with open(file_path, 'wb') as f:
                            f.write(normalized)
                        retorno.append(file_path)
                    except Exception as e:
                        logging.error('error rewriting file: {}'.format(file_path))
                        logging.error(e)
    return retorno


path = '/home/jose.runin/jose.runin_nfs/promocode_creator_dev/promocode_creator/common/helpers/thrift/idl/code.uber.internal'

logging.info('starting script main.py ' + 'with path ' + path)

rewrite_files_encoding(path)