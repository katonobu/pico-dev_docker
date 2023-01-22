#!/bin/bash

OUTDIR="$(pwd)/pico"

# Pick up new variables we just defined
source "$OUTDIR/pico_env_rc"

# Build a couple of examples
cd $OUTDIR
BUILDDIR="$OUTDIR/build_rzppw"
if [ -d $BUILDDIR ];then
    rm -rf $BUILDDIR
fi
mkdir $BUILDDIR
cd $BUILDDIR

# you must set WIFI_SSID,WIFI_PASSWORD to adjust your Wifi Environment if you use cyw43(Wifi)
cmake ../pico-examples_katonobu -DCMAKE_BUILD_TYPE=Debug -DPICO_BOARD=pico_w -DWIFI_SSID="SSID_STR" -DWIFI_PASSWORD="PASSWD_STR"
