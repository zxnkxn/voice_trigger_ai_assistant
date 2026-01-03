import yaml


def load_config(path="config.yml"):
    """Load YAML config and return it as a Python dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
