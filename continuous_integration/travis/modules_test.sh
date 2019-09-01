#!/usr/bin/env bash

set -ex

export TEST_CI_WIDGETS=True
export PYTHONPATH=.
export PATH="$HOME/miniconda/bin:$PATH"
source activate test

conda install -q qt=4.* pyqt=4.* qtconsole matplotlib

# Depth 1
for f in trex/*.py; do
    if [[ $f == *test*/test_* ]]; then
        continue
    fi
    if [[ $f == trex/pyplot.py ]]; then
        continue
    fi
    python "$f"
    if [ $? -ne 0 ]; then
        exit 1
    fi
done


# Depth 2
for f in trex/*/*.py; do
    if [[ $f == *test*/test_* ]]; then
        continue
    fi
    if [[ $f == trex/app/*.py ]]; then
        continue
    fi
    if [[ $f == trex/plugins/*.py ]]; then
        continue
    fi
    if [[ $f == trex/utils/inputhooks.py ]]; then
        continue
    fi
    if [[ $f == trex/utils/qthelpers.py ]]; then
        continue
    fi
    if [[ $f == trex/utils/windows.py ]]; then
        continue
    fi
    # TODO: Understand why formlayout is failing in Travis!!
    if [[ $f == trex/widgets/formlayout.py ]]; then
        continue
    fi
    python "$f"
    if [ $? -ne 0 ]; then
        exit 1
    fi
done


# Depth 3
for f in trex/*/*/*.py; do
    if [[ $f == *test*/test_* ]]; then
        continue
    fi
    if [[ $f == trex/external/*/*.py ]]; then
        continue
    fi
    if [[ $f == trex/utils/external/*.py ]]; then
        continue
    fi
    if [[ $f == trex/utils/help/*.py ]]; then
        continue
    fi
    if [[ $f == trex/utils/ipython/start_kernel.py ]]; then
        continue
    fi
    if [[ $f == trex/utils/ipython/trex_kernel.py ]]; then
        continue
    fi
    if [[ $f == trex/utils/site/sitecustomize.py ]]; then
        continue
    fi
    if [[ $f == trex/utils/introspection/plugin_client.py ]]; then
        continue
    fi
    if [[ $f == trex/widgets/externalshell/systemshell.py ]]; then
        continue
    fi
    if [[ $f == trex/widgets/ipythonconsole/__init__.py ]]; then
        continue
    fi
    python "$f"
    if [ $? -ne 0 ]; then
        exit 1
    fi
done


# Depth 4
for f in trex/*/*/*/*.py; do
    if [[ $f == *test*/test_* ]]; then
        continue
    fi
    python "$f"
    if [ $? -ne 0 ]; then
        exit 1
    fi
done


# TRexplugins
for f in trex_*/widgets/*.py; do
    if [[ $f == *test*/test_* ]]; then
        continue
    fi
    python "$f"
    if [ $? -ne 0 ]; then
        exit 1
    fi
done
