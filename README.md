# Wardoff

[![Build Status](https://travis-ci.org/4383/wardoff.svg?branch=master)](https://travis-ci.org/4383/wardoff)
![PyPI](https://img.shields.io/pypi/v/wardoff.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wardoff.svg)
![PyPI - Status](https://img.shields.io/pypi/status/wardoff.svg)
[![Downloads](https://img.shields.io/pypi/dm/wardoff.svg)](https://pypi.python.org/pypi/wardoff/)

Wardoff (pronounced `ward off`) aim to help you to maintain your code base
clean and up-to-date by reducing the pain of collect informations about all
your underlaying libraries in your stack in a proactively.

Wardoff looking for deprecated stuffs in project requirements and underlying
libraries to help you to keep your code up-to-date.

The main goal of wardoff is to analyze all requirements of a given project
to extract deprecated things from their codes.

For each analyze a dedicated python virtual environment is built and project's
requirements are installed within. Then installed source code files of
project's requirement are analyzed one by one.

Code analyze of the requirements is based on
[AST](https://docs.python.org/3/library/ast.html) and
[python tokens](https://docs.python.org/3/library/tokenize.html). Each
source code file of each underlaying library is analyzed in this way.

You can pass a list of constraints to apply to your analyze to be sure
to match the right versions of your underlaying libraries.

Traditionally projects maintainers are informed that functions will become
deprecated or removed by reading documentation or by
observing deprecation warning at the runtime in logs. When your stack
grow and the number of requirements in your stack increase it could be
painful to stay up-to-date, wardoff aim to collect for you all these infos
by only using 1 command without needing any runtime environment setup.



## Install

Still in development and really unstable, however you can install unstable
development versions by using:

```shell
$ python3 -m pip install --user wardoff
```

## Requirements

- python3.8+
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

## The future of wardoff

We plan to introduce more features like issues and pull requests or
patches harvesting.
