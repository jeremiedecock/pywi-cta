#!/bin/sh

echo
echo "PyWI version:"
python3 -c "from pywi import get_version ; print(get_version())"

echo
echo "PyWI-CTA version:"
python3 -c "from pywicta import get_version ; print(get_version())"

# DOCTESTS ####################################################################

echo
echo
python3 -m doctest ./pywicta/io/images.py
if [ $? -ne 0 ]; then
    exit 1
fi

# UNITTESTS ###################################################################

pytest
