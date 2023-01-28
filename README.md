# poetry-watsin

Simple poetry plugin to show the available extras (optional dependencies) of a particular python package.

## Installation

```bash
$ poetry self add git+https://github.com/DeviousStoat/poetry-watsin
```

## Usages

```bash
$ poetry watsin --help

 Description:
  Shows the available `extras` (optional dependencies) in a particular python package

Usage:
  watsin [options] [--] <package_name> [<package_version>]

Arguments:
  package_name               The name of the package
  package_version            The version of the package. If not provided will check the latest version
```


```bash
$ poetry watsin black
colorama :
   * colorama (>=0.4.3)
d :
   * aiohttp (>=3.7.4)
jupyter :
   * ipython (>=7.8.0)
   * tokenize-rt (>=3.2.0)
uvloop :
   * uvloop (>=0.15.2)
```
