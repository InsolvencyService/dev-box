#!/usr/bin/env bash

echo "This will be replaced by ./go.sh very soon"
echo "This will be replaced by ./go.sh very soon"
echo "This will be replaced by ./go.sh very soon"
echo "This will be replaced by ./go.sh very soon"
echo "This will be replaced by ./go.sh very soon"
echo "This will be replaced by ./go.sh very soon"

set -oe pipefail

PATH=$PATH:$(pwd)
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $PROJECT_ROOT

./ensure_clean_tables

nosetests --exe

behave -q --tags=-wip --stop feature_tests/
