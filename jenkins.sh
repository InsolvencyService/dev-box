#!/usr/bin/env bash

set -e
set -x


VENVNAME=rps-dev

if [ -z "$VIRTUAL_ENV" -a -n "$WORKON_HOME" ]; then

  venvdir=$WORKON_HOME/$VENVNAME

  if [ ! -d "$venvdir" ]; then
    virtualenv $venvdir
  fi

  source "$venvdir/bin/activate"

  # meh - see https://github.com/pypa/pip/issues/56
  pip install -r rps/requirements.dev.txt
fi

cd rps

# FIXME: Shouldn't have to run ensure_clean_tables before unit tests

./ensure_clean_tables

nosetests --exe --with-xunit

behave -q --tags=-wip --stop feature_tests/
