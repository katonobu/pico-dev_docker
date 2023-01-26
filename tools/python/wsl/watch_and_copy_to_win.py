import os
import time
import datetime
import shutil

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

class FileStt():
    _build_base_path = None
    _target_path = None

    @classmethod
    def set_build_base_path(cls, build_base_path):
        cls._build_base_path = build_base_path

    @classmethod
    def set_target_path(cls, target_path):
        cls._target_path = target_path

    def __init__(self, src_file):
        self.src_file_path = os.sep.join([FileStt._build_base_path, src_file])
        if os.path.isfile(self.src_file_path):
            stat = os.stat(self.src_file_path)
            self.current_ts = stat.st_mtime
            self.prev_ts = stat.st_mtime
        else:
            self.current_ts = 0
            self.prev_ts = 0

    def update(self):
        updated = False
        if os.path.isfile(self.src_file_path):
            stat = os.stat(self.src_file_path)
            self.prev_ts = self.current_ts
            self.current_ts = stat.st_mtime
            if self.prev_ts < self.current_ts:
                updated = True
        return updated

    def print(self):
        print("{}".format(self.src_file_path.split(os.sep)[-1]))
        if self.prev_ts is not None:
            print("  prev_ts   :{}".format(datetime.datetime.fromtimestamp(self.prev_ts).strftime('%Y/%m/%d %H:%M:%S')))
        else:
            print("  prev_ts   :None")
        if self.current_ts is not None:
            print("  current_ts:{}".format(datetime.datetime.fromtimestamp(self.current_ts).strftime('%Y/%m/%d %H:%M:%S')))
        else:
            print("  current_ts:None")

if __name__ == "__main__" :
    if not os.path.isdir(target_path):
        os.makedirs(target_path)

    FileStt.set_build_base_path(build_base_path)
    FileStt.set_target_path(target_path)

    fileStts = [FileStt(f) for f in uf2_paths]

    print("Start : {}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S')))
    while True:
        for fileStt in fileStts:
            if fileStt.update():
                fileStt.print()
                shutil.copyfile(fileStt.src_file_path, target_path + os.sep + fileStt.src_file_path.split(os.sep)[-1])
                print("------------")
        time.sleep(1)
