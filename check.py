import os

def try_ascii(data, encode):
    try:
        data.encode(encode)
        return True
    except UnicodeEncodeError:
        return False


def check_files_no_valid_encode(folder_path, ends_in = '.thrift', encode = 'ascii'):
    retorno = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.endswith(ends_in):
                print('opening file: {}'.format(file_path))
                with open(file_path, 'r') as f:
                    content = f.read()
                if not try_ascii(content, encode):
                    with open(file_path, 'r') as f:
                        content = f.readlines()
                    for i, line in enumerate(content):
                        try:
                            line.encode(encode)
                        except UnicodeEncodeError:
                            print('file: {}\n linenumber: {}\n line: {}\n\n'.format(file_path, i+1, line))

    return

path = '/home/jose.runin/jose.runin_nfs/testing_folder'
check_files_no_valid_encode(path, '')