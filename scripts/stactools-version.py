from setuptools.config import pyprojecttoml

conf_dict = pyprojecttoml.load_file("pyproject.toml")

# Filter out entries that don't start with 'stactools ' or 'stactools['.
# Split the entry on whitespace and select the last item which should be the version.
version = (
    [
        req
        for req in conf_dict["project"]["dependencies"]
        if req.startswith("stactools ") or req.startswith("stactools[")
    ][0]
    .split()
    .pop()
)

print(version)
