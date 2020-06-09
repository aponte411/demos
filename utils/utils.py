import os


def setup_file(file_path: str, overwrite: bool = False):
    dirname = os.path.dirname(file_path)
    if len(dirname) > 0 and not os.path.exists(dirname):
        os.makedirs(dirname)

    if os.path.exists(file_path):
        if overwrite:
            os.remove(file_path)
        else:
            raise Exception(f"{file_path} already exists, use overwrite flag.")
