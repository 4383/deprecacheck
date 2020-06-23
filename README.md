# Wardoff

Looking for deprecated stuffs in project requirements and underlying libraries

Pronounced `ward off`

## Install

Still in development will be released on pypi soon.

## Requirements

- python
- git

## Usages

### From a named package

Found deprecated things from a named package (directly from pypi):

```sh
$ wardoff niet # will list all deprecations founds in niet is requirements
$ wardoff oslo.messaging # will list all deprecations founds in oslo.messaging is requirements
```

### From the current directory

Retrieve deprecated things from the current working directory.
Retrieve requirements from:
- `requirements.txt`
- `test-requirements.txt`
- `*-requirements.txt`

Example:

```sh
$ wardoff # will list all deprecations founds in requirements founds in current directory
```

### From a distant repository

Retrieve deprecated things from a distgit repo.

Example:

```sh
$ wardoff https://opendev.org/openstack/nova/ # from opendev.org
$ wardoff https://github.com/openstack/nova # from github.com
$ wardoff git@github.com:openstack/nova # by using git format
```

### From a local repository

Retrieve deprecated things from a distgit repo.

Example:

```sh
$ wardoff ~/dev/nova # from a local clone of openstack/nova
```
