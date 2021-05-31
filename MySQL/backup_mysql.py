import yaml
import os

print("Hallo")
"""
--single-transaction uses a consistent read and guarantees that data seen by mysqldump does not change.

Backup in single Files

for DB in $(mysql - u root - p mysqlmaster - e 'show databases' - s - -skip-column-names)
do
mysqldump $DB > "$DB.sql"
done
"""


def load_yml():
    """
    Load the yaml file config.yaml
    """
    with open('config.yaml', 'rt') as f:
        yml = yaml.safe_load(f.read())
    return yml


if __name__ == "__main__":
    config = load_yml()
    print(config)
