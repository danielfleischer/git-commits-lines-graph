# Git Commit Lines Graph

[![PyPI](https://img.shields.io/pypi/v/git-lines-graph?color=brightgreen)](https://pypi.org/project/git-lines-graph/)
[![Python Version](https://img.shields.io/pypi/pyversions/git-lines-graph?color=orange)](https://pypi.org/project/git-lines-graph/)
[![License: GPL v3+](https://img.shields.io/badge/License-GPLv3+-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Downloads](https://img.shields.io/pypi/dm/git-lines-graph?color=red)](https://pypi.org/project/git-lines-graph/)

A small python script to visualize the number of lines in a project, as a function of time.

<img src="https://raw.githubusercontent.com/danielfleischer/git-commits-lines-graph/master/example.png" width="400" align="center">

## Install

```sh
uv tool install git-lines-graph   
# OR
python3 -m pip install git-lines-graph
```

## Usage

Run: `git-lines-graph [-b BRANCH] [GIT-DIR]`

Call with an optional git project directory. You can also specify a branch to scan; other wise the branch currently checked in is used.

## Dependencies

- `GitPython` to interact with `git`.
- `matplotlib` for plotting.
- `pandas` for data manipulation.

----

### How Does It Work

The code goes over all commits messages and looks for the number of lines added/removed and keeps an updated count. **Caveat**: the lines reported in git commit messages are only a proxy for the true number of lines of code. It could be way off in projects in which there are data artifacts such as big data files. One solution is to loop over all commits, checkout the commit and do a `wc` over all files that are considered to be code files. But that's slower and could be dangerous in dirty projects.
