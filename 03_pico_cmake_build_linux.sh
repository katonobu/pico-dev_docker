#!/bin/bash

OUTDIR="$(pwd)/pico"

# Pick up new variables we just defined
source "$OUTDIR/pico_env_rc"

# Build a couple of examples
cd $OUTDIR
BUILDDIR="$OUTDIR/build_linux"
if [ -d $BUILDDIR ];then
    rm -rf $BUILDDIR
fi
mkdir $BUILDDIR
cd $BUILDDIR

cmake ../pico-examples_katonobu -DCMAKE_BUILD_TYPE=Debug -DPICO_BOARD=pico_w -DPICO_PLATFORM=host

for e in hello_world divider
do
    echo "Building $e"
    cd $e
    make -j$JNUM
    cd ..
done

cd $OUTDIR
build_linux/divider/hello_divider
build_linux/hello_world/serial/hello_serial