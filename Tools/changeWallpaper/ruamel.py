import os
from pathlib import Path
import sys

import ruamel.yaml


yaml_str = """\
# Our app configuration

# foo is our main variable
foo: bar

# foz is also important
foz: quz

# And finally we have our optional configs.
# These are not really mandatory, they can be
# considere as "would be nice".
opt1: foqz
"""

undefined = object()


def my_pop(data):
    keys = list(data.keys())
    print(data.ca.items)

    prev = keys[idx - 1]
    # print('prev', prev, self.ca)
    comment = data.ca.items.pop(key)[2]
    if prev in self.ca.items:
        data.ca.items[prev][2].value += comment.value
    else:
        data.ca.items[prev] = data.ca.items.pop(key)
    res = self.__getitem__(key)
    data.__delitem__(key)
    return res


yaml = ruamel.yaml.YAML()
data = yaml.load(yaml_str)
#data = my_pop(data)

#yaml.dump(data, sys.stdout)


rootDir = Path(__file__).parent
configFile = os.path.join(rootDir, 'config.yaml')
fp = open(configFile, "r")
yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
yaml.explicit_start = True

data = yaml.load(fp)
keys = list(data.keys())
print(keys)
data.ca
print(data)


#yaml.dump(data, sys.stdout)
