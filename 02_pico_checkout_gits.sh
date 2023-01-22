#!/bin/bash

# Exit on error
set -e

# Number of cores when running make
JNUM=4

# Where will the output go?
OUTDIR="$(pwd)/pico"

mkdir -p $OUTDIR

cd $OUTDIR

# Clone sw repos

#GITHUB_PREFIX="https://github.com/raspberrypi/"
#SDK_BRANCH="master"

GITHUB_PREFIX="https://github.com/katonobu/"
SDK_BRANCH="feature/tinyusb_net"

GITHUB_SUFFIX=".git"

#for REPO in sdk examples
for REPO in sdk_katonobu examples_katonobu
do
    DEST="$OUTDIR/pico-$REPO"

    if [ -d $DEST ]; then
        echo "$DEST already exists so skipping"
    else
        REPO_URL="${GITHUB_PREFIX}pico-${REPO}${GITHUB_SUFFIX}"
        echo "Cloning $REPO_URL"
        git clone -b $SDK_BRANCH $REPO_URL

        # Any submodules
        cd $DEST
        git submodule update --init
        cd $OUTDIR

        # Define PICO_SDK_PATH in ~/.bashrc
        TMP="PICO_${REPO^^}_PATH"
        VARNAME=${TMP//_KATONOBU/}
        echo "Adding $VARNAME to $OUTDIR/pico_env_rc"
        echo "export $VARNAME=$DEST" >> $OUTDIR/pico_env_rc
        export ${VARNAME}=$DEST
    fi
done

cd $OUTDIR

DEST="$OUTDIR/FreeRTOS-Kernel"

if [ -d $DEST ]; then
    echo "$DEST already exists so skipping"
else
    REPO_URL="https://github.com/FreeRTOS/FreeRTOS-Kernel"
    FREE_RTOS_BRANCH="main"

    echo "Cloning $REPO_URL"
    git clone -b $FREE_RTOS_BRANCH $REPO_URL

    # Define PICO_SDK_PATH in ~/.bashrc
    VARNAME=FREERTOS_KERNEL_PATH
    echo "Adding $VARNAME to $OUTDIR/pico_env_rc"
    echo "export $VARNAME=$DEST" >> $OUTDIR/pico_env_rc
    export ${VARNAME}=$DEST
fi


