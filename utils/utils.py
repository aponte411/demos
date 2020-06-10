import os

import joblib


def setup_file(file_path: str, overwrite: bool = False):
    dirname = os.path.dirname(file_path)
    if len(dirname) > 0 and not os.path.exists(dirname):
        os.makedirs(dirname)

    if os.path.exists(file_path):
        if overwrite:
            os.remove(file_path)
        else:
            raise Exception(f"{file_path} already exists, use overwrite flag.")


def download_from_s3(path):
    pass


def load_model(path: str):
    if path.startswith("s3://"):
        # load from s3 and save to local path
        download_from_s3(path=path)
        path = ""
        pass
    return joblib.load(path)
