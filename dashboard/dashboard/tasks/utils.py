import os
from zipfile import ZipFile


def compress(zipfn, dirname):
    with ZipFile(zipfn, "w") as zipfile:
        for current_folder, subfolders, files in os.walk(dirname):
            for file in subfolders + files:
                zipfile.write(os.path.join(current_folder, file))
        return zipfile
