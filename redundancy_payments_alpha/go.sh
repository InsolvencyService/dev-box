#!/usr/bin/env bash

PATH=$PATH:$(pwd)
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${PROJECT_ROOT}

JOB_DESC="None"
WARN=$(tput bold)$(tput setaf 1)
RESET=$(tput sgr0)
YAY=$(tput bold)$(tput setaf 3)


function warn_quit {
    echo "${WARN}[FAILED] $1"
    echo ""
    echo "BBBBB   UU   UU IIIII LL      DDDDD       FFFFFFF   AAA   IIIII LL      EEEEEEE DDDDD"
    echo "BB   B  UU   UU  III  LL      DD  DD      FF       AAAAA   III  LL      EE      DD  DD"
    echo "BBBBBB  UU   UU  III  LL      DD   DD     FFFF    AA   AA  III  LL      EEEEE   DD   DD"
    echo "BB   BB UU   UU  III  LL      DD   DD     FF      AAAAAAA  III  LL      EE      DD   DD"
    echo "BBBBBB   UUUUU  IIIII LLLLLLL DDDDDD      FF      AA   AA IIIII LLLLLLL EEEEEEE DDDDDD"
    echo "${RESET}"
    exit
}

function build_passed {
    echo "${YAY}"
    echo "BBBBB   UU   UU IIIII LL      DDDDD       PPPPPP    AAA    SSSSS   SSSSS  EEEEEEE DDDDD"
    echo "BB   B  UU   UU  III  LL      DD  DD      PP   PP  AAAAA  SS      SS      EE      DD  DD"
    echo "BBBBBB  UU   UU  III  LL      DD   DD     PPPPPP  AA   AA  SSSSS   SSSSS  EEEEE   DD   DD"
    echo "BB   BB UU   UU  III  LL      DD   DD     PP      AAAAAAA      SS      SS EE      DD   DD"
    echo "BBBBBB   UUUUU  IIIII LLLLLLL DDDDDD      PP      AA   AA  SSSSS   SSSSS  EEEEEEE DDDDDD"
    echo "${RESET}"
    exit
}

function passed {
    echo "${YAY}[PASSED] $1${RESET}"
}

function pass_fail {
    if [ "$?" -ne "0" ]; then warn_quit "$JOB_DESC"; else passed "$JOB_DESC"; fi
}

function check_for_tabs {
    JOB_DESC="Checking there are no tabs in html, python and feature files"
    ! find . -name "*.html" -o -name "*.py" -o -name "*.feature" | xargs grep -P '\t' --color=AUTO; pass_fail
}

function activate_venv {
    VENV_NAME="rps"
    JOB_DESC="Activating the virtual environment ($VENV_NAME)"
    INSIDE_VENV=`python -c "import sys; print hasattr(sys, 'real_prefix')"`

    if [ ${INSIDE_VENV} != "True" ]; then
    source "$HOME/.virtualenvs/$VENV_NAME/bin/activate" 2> /dev/null; pass_fail
    fi
}

function requirements {
    JOB_DESC="Installing requirements via pip"
    pip install -q -r requirements.dev.txt; pass_fail
}

function load_environment {
    JOB_DESC="Sourcing environment variables"
    source environment.sh; pass_fail
}

function unit_tests {
    JOB_DESC="Running unit tests"
    ./ensure_clean_tables
    nosetests -q --exe 1> unit_tests.log 2>&1; pass_fail
}

function feature_tests {
    JOB_DESC="Running feature tests"
    behave -q --tags=-wip --stop feature_tests/ 1> feature_tests.log 2>&1; pass_fail
}

function build {
    check_for_tabs
    activate_venv
    requirements
    unit_tests
    load_environment
    feature_tests
    build_passed
}

build
