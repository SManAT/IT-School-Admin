import sys
import ruamel.yaml
from libs.YamlRuamel import YamlRuamel

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

yaml = ruamel.yaml.YAML()
data = yaml.load(yaml_str)
print(type(ruamel.yaml.comments.CommentedMap))
cmnts = ruamel.yaml.comments.CommentedMap()
print(cmnts.keys())
"""


data.pop('foz', None)

yaml.dump(data, sys.stdout)
"""