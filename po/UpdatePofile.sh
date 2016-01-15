#!/bin/sh

VERS=2.7
TEMPDIR=/tmp/GvR_temp_4_po
echo "Saving your po tree to po.org"
cp -r ../po ../po.org

mkdir -p $TEMPDIR
python generate_pot.py ../ GvRng $VERS > $TEMPDIR/messages.po
echo "Placed a new pot file in ./po"
cp $TEMPDIR/messages.po GvRng_$VERS.pot
find . -name "*.po" | while read pofile
    do
	echo $pofile
        msgmerge --update --backup=off -i -s $pofile $TEMPDIR/messages.po
    done
