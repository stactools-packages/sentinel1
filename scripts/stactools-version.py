from setuptools.config import read_configuration

conf_dict = read_configuration("setup.cfg")

# Filter out entries that don't start with 'stactools ' or 'stactools['.
# Split the entry on whitespace and select the last item which should be the version.
version = [
    req for req in conf_dict['options']['install_requires']
    if req.startswith('stactools ') or req.startswith('stactools[')
][0].split().pop()

print(version)
