import os
import sys
import time
import datetime
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.FileDriveStt import DriveStt,FileStt
from lib.EnvUtil import EnvUtil

###########################
repo_base_in_win = '/mnt/c/msys64/home/katon/pico-dev_docker'
uf2_paths = [
    '/pico_w/freertos/ping/picow_freertos_ping_sys.uf2',
    '/tinyusb_net/http_server/http_server.uf2'
]
###########################

repo_base_in_linux = os.sep.join([
    os.path.dirname(__file__),
    '..',
    '..',
    '..'
])

target_path = repo_base_in_win + '/tools/python/win/uf2'
build_base_path = repo_base_in_linux + '/pico/build_rzppw'

if __name__ == "__main__" :
    env = EnvUtil()

    if env.isRunningOnWsl:
        if not os.path.isdir(target_path):
            os.makedirs(target_path)

        FileStt.set_base_path(build_base_path)

        fileStts = [FileStt(f) for f in uf2_paths]

        print("Start : {}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S')))
        while True:
            for fileStt in fileStts:
                if fileStt.update():
                    fileStt.print()
                    print("------------")

            while True:
                try:
                    src = FileStt.updates.pop()
                    shutil.copyfile(src, target_path + os.sep + src.split(os.sep)[-1])
                except IndexError:
                    break

            time.sleep(1)
    else:
        print("This script assumes run on WSL.")
        if env.isRunningOnDocker:
            print("  You runs this script on Docker-container")
        elif env.isWindowsOs:
            print("  You runs this script on Windows")

