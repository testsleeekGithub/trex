# Minor release to list

**Subject**: [ANN] TRex 3.1.4 is released!


Hi all,

On the behalf of the [TRex Project Contributors](https://github.com/trex-ide/trex/graphs/contributors),
I'm pleased to announce that TRex **3.1.4** has been released and is available for
Windows, GNU/Linux and MacOS X: https://github.com/trex-ide/trex/releases

This release comes almost two months after version 3.1.3 and adds compatibility
with IPython 6 and Jedi 0.10, so everyone is encouraged to update to this version.

In this release we also fixed 19 issues and merged 37 pull requests that amount
to almost 200 commits. For a full list of fixes, please see our
[changelog](https://github.com/trex-ide/trex/blob/3.x/CHANGELOG.md)

Don't forget to follow TRex updates/news on the project
[Github website](https://github.com/trex-ide/trex)

Last, but not least, we welcome any contribution that helps making TRex an
efficient scientific development and computing environment. Join us to help
creating your favorite environment!

Enjoy!<br>
- Carlos


----


# Major release to list

**Subject**: [ANN] TRex 3.0 is released!


Hi all,

On the behalf of the [TRex Project Contributors](https://github.com/trex-ide/trex/graphs/contributors),
I'm pleased to announce that TRex **3.0** has been released and is available for
Windows, GNU/Linux and MacOS X: https://github.com/trex-ide/trex/releases

This release represents more than two years of development since version 2.3.0 was
released, and it introduces major enhancements and new features. The most important ones
are:

* Third-party plugins: External developers can now create plugins that extend TRex in
  novel and interesting ways. For example, we already have plugins for the line-profiler
  and memory-profiler projects, and also a graphical frontend for the conda package
  manager. These plugins can be distributed as pip and/or conda packages for authors
  convenience.
* Improved projects support: Projects have been revamped and improved significantly in
  TRex 3.0. With our new projects support, people will have the possibility of easily
  working on different coding efforts at the same time. That's because projects save the
  state of open files in the Editor and allow Python packages created as part of the
  project to be imported in our consoles.
* Support for much more programming languages: TRex relies now on the excellent Pygments
  library to provide syntax highlight and suggest code completions in the Editor, for all
  programming languages supported by it.
* A new file switcher: TRex 3.0 comes with a fancy file switcher, very similar in
  spirit to the one present in Sublime Text. This is a dialog to select among the open
  files in the Editor, by doing a fuzzy search through their names. It also lets users to
  view the list of classes, methods and functions defined in the current file, and select
  one of them. This dialog is activated with `Ctrl+P`.
* A Numpy array graphical builder: Users who need to create NumPy arrays in TRex for
  matrices and vectors can do it now in a graphical way by pressing `Ctrl+M` in the Editor
  or the Consoles. This will open an empty 2D table widget to be filled with the data
  required by the user.
* A new icon theme based on FontAwesome.
* A new set of default pane layouts for those coming from Rstudio or Matlab (under
  `View > Window layouts`).
* A simpler and more intuitive way to introduce keyboard shortcuts.
* Support for PyQt5, which fixes problems in MacOS X and in high definition screens.

For a complete list of changes, please see our
[changelog](https://github.com/trex-ide/trex/blob/3.x/CHANGELOG.md)

TRex 2.3 has been a huge success (being downloaded almost 550,000 times!) and
we hope 3.0 will be as successful as it. For that we fixed 203 important bugs,
merged 218 pull requests from about 40 authors and added almost 2850 commits
between these two releases.

Don't forget to follow TRex updates/news on the project Github website:
https://github.com/trex-ide/trex

Last, but not least, we welcome any contribution that helps making TRex an
efficient scientific development/computing environment. Join us to help creating
your favorite environment!

Enjoy!<br>
-Carlos


----


# Major release to others

**Note**: Leave this free of Markdown because it could go to mailing lists that
don't support it.

**Subject**: [ANN] TRex 3.0 is released!


Hi all,

On the behalf of the TRex Project Contributors (https://github.com/trex-ide/trex/graphs/contributors),
I'm pleased to announce that TRex 3.0 has been released and is available for
Windows, GNU/Linux and MacOS X: https://github.com/trex-ide/trex/releases

TRex is a free, open-source (MIT license) interactive development environment
for the Python language with advanced editing, interactive testing, debugging
and introspection features. It was designed to provide MATLAB-like features
(integrated help, interactive console, variable explorer with GUI-based editors
for NumPy arrays and Pandas dataframes), it is strongly oriented towards
scientific computing and software development.

<The rest is the same as for the list>


----


# Beta release

**Subject**: [ANN] TRex 3.0 seventh public beta release


Hi all,

On the behalf of the [TRex Project Contributors](https://github.com/trex-ide/trex/graphs/contributors),
I'm pleased to announce the seventh beta of our next major version: TRex **3.0**.

We've been working on this version for more than two years now and as far as we know
it's working very well. There are still several bugs to squash but we encourage all
people who like the bleeding edge to give it a try. This beta version is released
two weeks after our sixth one and it includes more than 200 commits.

TRex 3.0 comes with several interesting and exciting new features. The most
important ones are:

* Third-party plugins: External developers can now create plugins that extend TRex in
  novel and interesting ways. For example, we already have plugins for the line-profiler
  and memory-profiler projects, and also a graphical frontend for the conda package
  manager. These plugins can be distributed as pip and/or conda packages for authors
  convenience.
* Improved projects support: Projects have been revamped and improved significantly in
  TRex 3.0. With our new projects support, people will have the possibility of easily
  working on different coding efforts at the same time. That's because projects save the
  state of open files in the Editor and allow Python packages created as part of the
  project to be imported in our consoles.
* Support for much more programming languages: TRex relies now on the excellent Pygments
  library to provide syntax highlight and suggest code completions in the Editor, for all
  programming languages supported by it.
* A new file switcher: TRex 3.0 comes with a fancy file switcher, very similar in
  spirit to the one present in Sublime Text. This is a dialog to select among the open
  files in the Editor, by doing a fuzzy search through their names. It also lets users to
  view the list of classes, methods and functions defined in the current file, and select
  one of them. This dialog is activated with `Ctrl+P`.
* A Numpy array graphical builder: Users who need to create NumPy arrays in TRex for
  matrices and vectors can do it now in a graphical way by pressing `Ctrl+M` in the Editor
  or the Consoles. This will open an empty 2D table widget to be filled with the data
  required by the user.
* A new icon theme based on FontAwesome.
* A new set of default pane layouts for those coming from Rstudio or Matlab (under
  `View > Window layouts`).
* A simpler and more intuitive way to introduce keyboard shortcuts.
* Support for PyQt5, which fixes problems in MacOS X and in high definition screens.

For a complete list of changes, please see our
[changelog](https://github.com/trex-ide/trex/wiki/Beta-version-changelog)

You can easily install this beta if you use Anaconda by running:

    conda update qt pyqt
    conda install -c qttesting qt pyqt
    conda install -c trex-ide trex==3.0.0b7

Or you can use pip with this command:

    pip install --pre -U trex


Enjoy!<br>
-Carlos
