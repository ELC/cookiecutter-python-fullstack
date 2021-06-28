import shutil
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

from common import EXTRA, PARAMS, OUTPUT_DIR


@pytest.fixture(autouse=True)
def post_build():
    if Path(OUTPUT_DIR).is_dir():
        shutil.rmtree(OUTPUT_DIR)
    yield

    shutil.rmtree(OUTPUT_DIR)


licenses_combinations = {
    "MIT": "Permission is hereby granted",
    "BSD-3-Clause": "Redistribution and use in source and binary forms",
    "Apache-2.0": "Licensed under the Apache License",
    "Skip": "All Rights Reserved.",
}


@pytest.mark.parametrize("license, first_line", licenses_combinations.items())
def test_license_mit(license, first_line):
    author = "John Doe"
    year = "2021"
    overwrite_backend = dict(app_license=license, app_author=author, app_year=year)
    overwrite = dict(EXTRA, **overwrite_backend)
    cookiecutter(".", extra_context=overwrite, **PARAMS)
    license_path = Path(OUTPUT_DIR, "LICENSE")

    assert license_path.is_file()

    with open(license_path) as license_file:
        lines = license_file.readlines()

    header = lines[0]
    assert author in header and year in header

    content_first_line = lines[2]
    assert first_line in content_first_line
