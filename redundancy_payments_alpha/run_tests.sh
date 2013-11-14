#!/usr/bin/env bash

set -oe pipefail

PATH=$PATH:$(pwd)
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $PROJECT_ROOT

nosetests --exe

behave -q --tags=-wip --stop feature_tests/
