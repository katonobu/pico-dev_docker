# How to use.
1. Start docker from VS-Code
1. Run 01_pico_tools_setup.sh, this installs tools to be required for building Raspberrypi pico
1. Run 02_pico_checkout_gits.sh, this checks out git repository 
1. Run 03_pico_cmake_build_linux.sh, this builds for exectable binary for linux.
1. Run 04_pico_cmake_picow.sh, this makes makefiles for each project
1. After running 04_pico_cmake_picow.sh you can build each project as follows
```
vscode ➜ /workspaces/pico-dev_docker (master) $ cd pico/build_rzppw/
vscode ➜ .../pico/build_rzppw/hello_world/serial (master) $ cd hello_world/serial/
vscode ➜ .../pico/build_rzppw/hello_world/serial (master) $ make
:
Building C object hello_world/serial/CMakeFiles/hello_serial.dir/workspaces/pico-dev_docker/pico/pico-sdk_katonobu/src/rp2_common/pico_stdio_uart/stdio_uart.c.obj
Linking CXX executable hello_serial.elf
Built target hello_serial
vscode ➜ .../pico/build_rzppw/hello_world/serial (master) $ ls
CMakeFiles  cmake_install.cmake  hello_serial.bin  hello_serial.dis  hello_serial.elf  hello_serial.elf.map  hello_serial.hex  hello_serial.uf2  Makefile
```
now 
pico/build_rzppw/hello_world/serial/hello_serial.uf2
exist.
Copy this to Raspberrypi pico and check it works.
