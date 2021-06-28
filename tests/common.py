import sys

OUTPUT_DIR = "test_run"
EXTRA = dict(
    app_name=OUTPUT_DIR,
    app_python_version=f"{sys.version_info.major}.{sys.version_info.minor}",
)
PARAMS = dict(no_input=True, overwrite_if_exists=True)
