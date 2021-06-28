### Change Folders

import os
from pathlib import Path
import shutil

BACKEND = '{{ cookiecutter.app_backend|lower }}'
FRONTEND = '{{ cookiecutter.app_frontend|lower }}'
DATABASE_SELECTED = '{{ cookiecutter.app_database|lower }}'


if "document" in DATABASE_SELECTED:
    DATABASE = "document"
elif "cache" in DATABASE_SELECTED:
    DATABASE = "cache"
elif "object" in DATABASE_SELECTED:
    DATABASE = "object"
elif "sql" in DATABASE_SELECTED:
    DATABASE = "sql"


prefixes = ["backends", "frontends", "databases"]
directories = []
for prefix in prefixes:
    auxiliary = [Path(prefix, directory) for directory in os.listdir(prefix)]
    directories.extend(auxiliary)

for path in directories:
    # path = Path(directory)
    directory = path.stem
    is_frontend = directory.startswith("frontend")
    is_backend = directory.startswith("backend")
    is_database = directory.startswith("data")

    if not path.is_dir() or (not is_frontend and not is_backend and not is_database):
        continue
        
    if all(not directory.endswith(key) for key in [BACKEND, FRONTEND, DATABASE]):
        shutil.rmtree(path)
        continue

    if is_frontend:
        shutil.move(path, "frontend")
        continue

    if is_backend:
        shutil.move(path, "backend")
        continue

    if is_database:
        destination_path = Path("backend/app/data")
        if destination_path.is_dir():
            shutil.rmtree(destination_path)
        shutil.move(path, destination_path)
        continue

### Clean up

for prefix in prefixes:
    shutil.rmtree(prefix)


### Remove Paths

from pathlib import Path
import shutil

REMOVE_PATHS = [
    '{% if cookiecutter.app_dependency_manager != "pip" %} backend/requirements.txt {% endif %}',
    '{% if cookiecutter.app_dependency_manager != "pipenv" %} backend/Pipfile {% endif %}',
]

for path in REMOVE_PATHS:
    path_raw = path.strip()

    if not path_raw:
        continue

    path = Path(path_raw)
    
    if path.is_file():
        path.unlink()
    
    if path.is_dir():
        shutil.rmtree(path)
