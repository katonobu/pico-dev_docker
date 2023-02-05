import os
import wget
import json
import queue
import sys
import time
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.IpAddressUtil import specified_ipaddress_exist

def compare_wget_and_ref(url, ref_file_path):
    result = True
    print("Start download from {}".format(url))
    file_name = wget.download(url)
    print("")
    print("filename = {}".format(file_name))
    if os.path.isfile(file_name):
        with open(file_name) as f_act:
            act_lines = f_act.readlines()
            with open(ref_file_path) as f_ref:
                ref_lines = f_ref.readlines()
                if len(act_lines) == len(ref_lines):
                    for count in range(len(act_lines)):
                        if ref_lines[count].strip() != act_lines[count].strip():
                            result = False
                            break
                else:
                    print("act_lines_len = {}, ref_lines_len = {}".format(len(act_lines), len(ref_lines)))
                    result = False
        os.remove(file_name)
    else:
        print("File {} not exist".format(file_name))
        result = False
    return result


def http_server(file_path, msg_queue):
    result = False
    print("Test start for {}".format(file_path.split(os.sep)[-1]))
    ref_file_path = None
    url = None
    while True:
        try:
            rx_str = msg_queue.get(block=False)
            print("SerRx:{}".format(rx_str))
            if rx_str.startswith('reboot...'):
                break
            elif rx_str.startswith("IP:"):
                ip_address = rx_str.split(':')[-1].strip()
                ref_file_path = os.path.join(os.path.dirname(__file__), 'ref','index.html')
                url = 'http://{}'.format(ip_address)
            elif rx_str.startswith("DHCP : ") and result == False:
                ip_address = rx_str.split(':')[-1].strip()
                while True:
                    if specified_ipaddress_exist(ip_address) and ref_file_path and url:
                        try:
                            result = compare_wget_and_ref(url + '/index.html', ref_file_path)
                            requests.post(url, data={})
                        except ConnectionAbortedError as e:
                            print(e)

                        break
                    time.sleep(0.01)
        except queue.Empty:
            pass
        time.sleep(0.001)
    print("Result:{}".format("PASS" if result else "FAIL"))    
    print("finished")


def tls_client(file_path, msg_queue):
    print("Test start for {}".format(file_path.split(os.sep)[-1]))
    while True:
        try:
            rx_str = msg_queue.get(block=False)
            print("SerRx:{}".format(rx_str))
            if rx_str.startswith('reboot...'):
                break
            elif rx_str.startswith('{"ab'):
                rx_obj = json.loads(rx_str)
                time_diff = time.time() - rx_obj['unixtime']
                print("time.time() - rx.unix_time:{}  ".format(time_diff), end = "")
                print("{}".format("OK" if time_diff < 3 else "Too big diff"))

        except queue.Empty:
            pass
        time.sleep(0.001)
    print("finished")

def dummy(file_path, msg_queue):
    print("Test start for {}".format(file_path.split(os.sep)[-1]))
    while True:
        try:
            rx_str = msg_queue.get(block=False)
            print("SerRx:{}".format(rx_str))
            if rx_str.startswith('reboot...'):
                break
        except queue.Empty:
            pass
        time.sleep(0.001)
    print("finished")

def empty(file_path, msg_queue):
    print("Test start for {}".format(file_path.split(os.sep)[-1]))
    print("finished")

src_base_path = r'\\wsl.localhost\Ubuntu-22.04\home\katonobu'
src_files = [
    {
        'file':r'\pico-dev_docker_mqtt\pico\build_rzppw\pico_w\freertos\ping\picow_freertos_ping_sys.uf2',
        'func':dummy
    },{
        'file':r'\pico-dev_docker_mqtt\pico\build_rzppw\pico_w\freertos\mqtt\picow_freertos_mqtt_sys.uf2',
        'func':dummy
    },{
        'file':r'\pico-dev_docker_mqtt\pico\build_rzppw\pico_w\freertos\httpc\picow_freertos_httpc_sys.uf2',
        'func':dummy
    },{
        'file':r'\pico-dev_docker_mqtt\pico\build_rzppw\cunit\pico_cunit_example_basic.uf2',
        'func':dummy
    },{
        'file':r'\pico-dev_docker_usb_net\pico\build_rzppw\tinyusb_net\http_server\http_server.uf2',
        'func':http_server
    },{
        'file':r'\pico-dev_docker_usb_net\pico\build_rzppw\tinyusb_net\mqtt\mqtt.uf2',
        'func':empty
    },{
        'file':r'\pico-dev_docker_tls\pico\build_rzppw\pico_w\tls_client\picow_tls_client_background.uf2',
        'func':tls_client
    },{
        'file':r'\pico-dev_docker_mqtt\pico\build_rzppw\hello_world\serial\hello_serial.uf2',
        'func':dummy
    },{
        'file':r'\nuttx\pico\nuttx\nuttx.uf2',
        'func':dummy
    }
]
