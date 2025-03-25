#!/bin/bash
SCRIPT_PATHDIR="$(realpath $(dirname $BASH_SOURCE))"
cd ${SCRIPT_PATHDIR}

set -e # exit immediately if an error is encountered
set -x # print all commands before execution

INKSCAPE="/Applications/Inkscape.app/Contents/MacOS/inkscape"
GS="/opt/homebrew/bin/gs"
for fname in figs/*.svg
do
    $INKSCAPE "--export-filename=${fname}.eps" --export-ignore-filters --export-ps-level=3 --export-text-to-path "${fname}" 2>/dev/null
done

