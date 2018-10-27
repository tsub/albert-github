#!/bin/sh -eu

PLUGIN_PATH="$HOME/.local/share/albert/org.albert.extension.python/modules/GitHub"

if [ -d $PLUGIN_PATH ]; then
  exit
fi

ln -s $PWD/GitHub $PLUGIN_PATH
