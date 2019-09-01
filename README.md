# TRex - The Scientific PYthon Development EnviRonment

Copyright © TRex Project Contributors.

## Project details
[![license](https://img.shields.io/pypi/l/trex.svg)](./LICENSE)
[![pypi version](https://img.shields.io/pypi/v/trex.svg)](https://pypi.python.org/pypi/trex)
[![Join the chat at https://gitter.im/trex-ide/public](https://badges.gitter.im/trex-ide/trex.svg)](https://gitter.im/trex-ide/public)

## Build status
[![Travis status](https://travis-ci.org/trex-ide/trex.svg?branch=master)](https://travis-ci.org/trex-ide/trex)
[![AppVeyor status](https://ci.appveyor.com/api/projects/status/tvjcqa4kf53br8s0/branch/master?svg=true)](https://ci.appveyor.com/project/trex-ide/trex/branch/master)
[![CircleCI](https://circleci.com/gh/trex-ide/trex.svg?style=svg)](https://circleci.com/gh/trex-ide/trex)
[![Coverage Status](https://coveralls.io/repos/github/trex-ide/trex/badge.svg?branch=master)](https://coveralls.io/github/trex-ide/trex?branch=master)

## Overview

![screenshot](./img_src/screenshot.png)

TRex is a Python development environment with a lot of features:

* **Editor**

    Multi-language editor with function/class browser, code analysis
    features (pyflakes and pylint are currently supported), code
    completion, horizontal and vertical splitting, and goto definition.

* **Interactive console**

    Python or IPython consoles with workspace and debugging support to
    instantly evaluate the code written in the Editor. It also comes
    with Matplotlib figures integration. 

* **Documentation viewer**

    Show documentation for any class or function call made either in the
    Editor or a Console.

* **Variable explorer**

    Explore variables created during the execution of a file. Editing
    them is also possible with several GUI based editors, like a
    dictionary and Numpy array ones.

* **Find in files**

    Supporting regular expressions and mercurial repositories

* **File explorer**

* **History log**

TRex may also be used as a PyQt5/PyQt4 extension library (module
`trex`). For example, the Python interactive shell widget used in
TRex may be embedded in your own PyQt5/PyQt4 application.


## Documentation

You can read the TRex documentation at:

http://pythonhosted.org/trex/


## Installation

This section explains how to install the latest stable release of
TRex. If you prefer testing the development version, please use
the `bootstrap` script (see next section).

The easiest way to install TRex is:

### On Windows:

Using one (and only one) of these scientific Python distributions:

1. [Anaconda](http://continuum.io/downloads)
2. [WinPython](https://winpython.github.io/)
3. [Python(x,y)](http://python-xy.github.io)

### On Mac OSX:

- Using our DMG installer, which can be found
  [here](https://github.com/trex-ide/trex/releases).
- Using the [Anaconda Distribution](http://continuum.io/downloads).
- Through [MacPorts](http://www.macports.org/).

### On GNU/Linux

- Through your distribution package manager (i.e. `apt-get`, `yum`,
  etc).
- Using the [Anaconda Distribution](http://continuum.io/downloads).
- Installing from source (see below).

### Cross-platform way from source

You can also install TRex with the `pip` package manager, which comes by
default with most Python installations. For that you need to use the
command:

    pip install trex

To upgrade TRex to its latest version, if it was installed before, you need
to run

    pip install --upgrade trex

For more details on supported platforms, please refer to our
[installation instructions](http://pythonhosted.org/trex/installation.html).

**Important note**: This does not install the graphical Python libraries (i.e.
PyQt5 or PyQt4) that TRex depends on. Those have to be installed separately
after installing Python.


## Running from source

The fastest way to run TRex is to get the source code using git, install
PyQt5 or PyQt4, and run these commands:

1. Install our *runtime dependencies* (see below).
2. `cd /your/trex/git-clone`
3. `python bootstrap.py`

You may want to do this for fixing bugs in TRex, adding new
features, learning how TRex works or just getting a taste of it.


## Dependencies

**Important note**: Most if not all the dependencies listed below come
with *Anaconda*, *WinPython* and *Python(x,y)*, so you don't need to install
them separately when installing one of these Scientific Python
distributions.

### Build dependencies

When installing TRex from its source package, the only requirement is to have
a Python version greater than 2.7 (Python 3.2 is not supported anymore).

### Runtime dependencies

* **Python** 2.7 or 3.3+
* **PyQt5** 5.2+ or **PyQt4** 4.6+: PyQt5 is recommended.
* **qtconsole** 4.2.0+: Enhanced Python interpreter.
* **Rope** and **Jedi**: Editor code completion, calltips
  and go-to-definition.
* **Pyflakes**: Real-time code analysis.
* **Sphinx**: Rich text mode for the Help pane.
* **Pygments** 2.0+: Syntax highlighting for all file types it supports.
* **Pylint**: Static code analysis.
* **Pep8**: Style analysis.
* **Psutil**: CPU and memory usage on the status bar.
* **Nbconvert**: Manipulation of notebooks in the Editor.
* **Qtawesome** 0.4.1+: To have an icon theme based on FontAwesome.
* **Pickleshare**: Show import completions on the Python consoles.
* **PyZMQ**: Run introspection services asynchronously.
* **QtPy** 1.1.0+: Abstracion layer for Python Qt bindings so that TRex can run on PyQt4
  and PyQt5.
* **Chardet**: Character encoding auto-detection in Python.
* **Numpydoc**: Used by Jedi to get return types for functions with Numpydoc docstrings.

### Optional dependencies

* **Matplotlib**: 2D/3D plotting in the Python and IPython consoles.
* **Pandas**: View and edit DataFrames and Series in the Variable Explorer.
* **Numpy**: View and edit two or three dimensional arrays in the Variable Explorer.
* **SymPy**: Symbolic mathematics in the IPython console.
* **SciPy**: Import Matlab workspace files in the Variable Explorer.


## More information

* For code development please go to:

    <https://github.com/trex-ide/trex>

* For bug reports and feature requests:

    <https://github.com/trex-ide/trex/issues>

* For discussions and troubleshooting:

    <http://groups.google.com/group/trexlib>
