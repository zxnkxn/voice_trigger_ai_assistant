import os

import yaml


def load_config(path):
    """Load YAML config and return it as a Python dictionary."""
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(current_dir)
    # Construct the full path to the config file
    config_path = os.path.join(project_root, path)

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
