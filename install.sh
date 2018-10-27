#!/bin/sh -eu

PLUGIN_PATH="$HOME/.local/share/albert/org.albert.extension.python/modules/github.py"

if [ -f $PLUGIN_PATH ]; then
  exit
fi

ln -s $PWD/github.py $PLUGIN_PATH
