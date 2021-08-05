## Contributing

Pull Requests are the primary method of contributing to stactools-packages. Everyone is welcome to submit a stactools-package to describe their data. The intent with this project to get data which can be described by [STAC](https://stacspec.org/) to be built in an open and interoperable manner.

We consider everyone using the stactools-packages to be a 'contributor'.

## Deprecation

We recommend following the [Numpy Enhancement Proposals (NEP) 29](https://numpy.org/neps/nep-0029-deprecation_policy.html)
suggested deprecation policy for supported python versions.

>When a project releases a new major or minor version, we recommend that they support at least all minor versions of Python introduced and released in the prior 42 months from the anticipated release date with a minimum of 2 minor versions of Python, and all minor versions of NumPy released in the prior 24 months from the anticipated release date with a minimum of 3 minor versions of NumPy.

## Submitting Pull Requests

Any proposed changes to an existing stactools-packages should be done as pull requests. Please make these
requests against the `main` branch (unless otherwise directed by the dataset maintainer).

Creating a Pull Request will show our PR template, which includes checkbox reminders for a number
of things.

- Adding an entry the [CHANGELOG](CHANGELOG.md). If the change is more editorial and minor then this is not required, but any change to the actual code should have one.
- Make a ticket in the stactools-package data specific repository which is tracked on the [project management board](https://github.com/orgs/stactools-packages/projects/1).
- Highlight if the PR makes breaking changes to the code.


---
Attribution:
- https://docs.github.com/en/communities/
- https://github.com/radiantearth/stac-spec/blob/master/CONTRIBUTING.md
