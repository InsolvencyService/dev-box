#!/usr/bin/env bash

VENVNAME=rps

if [ -z "$VIRTUAL_ENV" -a -n "$WORKON_HOME" ]; then

   venvdir=$WORKON_HOME/$VENVNAME

   if [ ! -d "$venvdir" ]; then
     virtualenv $venvdir
   fi

   source "$venvdir/bin/activate"

   pip install -r redundancy_payments_alpha/requirements.dev.txt

   cd redundancy_payments_alpha/
   ./ensure_clean_tables
   cd ..
fi
