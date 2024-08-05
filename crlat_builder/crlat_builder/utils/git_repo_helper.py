import os

import logging
from git import Repo
import shutil

logger = logging.getLogger(__name__)

def clone_repository(repository_url, branch='master', dest_path='./tmp/sources', clear_dest=True):
    if clear_dest:
        shutil.rmtree(dest_path, ignore_errors=True)
    os.makedirs(dest_path)
    Repo.clone_from(repository_url, dest_path, branch=branch)