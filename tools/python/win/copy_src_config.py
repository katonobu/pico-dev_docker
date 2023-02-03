import os

def dummy(file_path):
    print("=== exec : {} ====".format(file_path.split(os.sep)[-1]))

src_base_path = r'\\wsl.localhost\Ubuntu-22.04\home\katonobu'
src_files = [
    {
        'file':r'\pico-dev_docker\pico\build_rzppw\pico_w\freertos\ping\picow_freertos_ping_sys.uf2',
        'func':dummy
    },{
        'file':r'\pico-dev_docker\pico\build_rzppw\pico_w\freertos\mqtt\picow_freertos_mqtt_sys.uf2',
        'func':dummy
    },{
        'file':r'\pico-dev_docker\pico\build_rzppw\pico_w\freertos\httpc\picow_freertos_httpc_sys.uf2',
        'func':dummy
    },{
        'file':r'\pico-dev_docker\pico\build_rzppw\cunit\pico_cunit_example_basic.uf2',
        'func':dummy
    },{
        'file':r'\pico-dev_docker\pico\build_rzppw\cunit\pico_cunit_example_console.uf2',
        'func':dummy
    },{
        'file':r'\pico-dev_docker\pico\build_rzppw\hello_world\serial\hello_serial.uf2',
        'func':dummy
    },{
        'file':r'\nuttx\pico\nuttx\nuttx.uf2',
        'func':dummy
    }
]
