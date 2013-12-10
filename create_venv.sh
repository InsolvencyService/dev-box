#!/usr/bin/env bash

VENVNAME=rps

if [ -z "$VIRTUAL_ENV" -a -n "$WORKON_HOME" ]; then

   venvdir=$WORKON_HOME/$VENVNAME

   if [ ! -d "$venvdir" ]; then
     virtualenv $venvdir
   fi

   source "$venvdir/bin/activate"

   pip install -r rps/requirements.dev.txt

   cd rps/
   ./ensure_clean_tables
   cd ..
fi
