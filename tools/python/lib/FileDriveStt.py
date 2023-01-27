import os
import datetime

class FileStt():
    _base_path = None
    updates = []

    @classmethod
    def set_base_path(cls, base_path):
        cls._base_path = base_path

    def __init__(self, src_file):
        self.file_path = os.sep.join([FileStt._base_path, src_file])
        if os.path.isfile(self.file_path):
            stat = os.stat(self.file_path)
            self.current_ts = stat.st_mtime
            self.prev_ts = stat.st_mtime
        else:
            self.current_ts = 0
            self.prev_ts = 0

    def update(self):
        updated = False
        if os.path.isfile(self.file_path):
            stat = os.stat(self.file_path)
            self.prev_ts = self.current_ts
            self.current_ts = stat.st_mtime
            if self.prev_ts < self.current_ts:
                # if same entry exist in self.updates, remove it and append new one.
                if self.file_path in FileStt.updates:
                    FileStt.updates.remove(self.file_path)
                FileStt.updates.append(self.file_path)
                updated = True
        return updated

    def print(self):
        print("{}".format(self.file_path.split(os.sep)[-1]))
        if self.prev_ts is not None:
            print("  prev_ts   :{}".format(datetime.datetime.fromtimestamp(self.prev_ts).strftime('%Y/%m/%d %H:%M:%S')))
        else:
            print("  prev_ts   :None")
        if self.current_ts is not None:
            print("  current_ts:{}".format(datetime.datetime.fromtimestamp(self.current_ts).strftime('%Y/%m/%d %H:%M:%S')))
        else:
            print("  current_ts:None")

class DriveStt():
    @staticmethod
    def get_all_drives():
        return set([f'{d}:' for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f'{d}:')])

    def __init__(self):
        self.prev_drives = DriveStt.get_all_drives()
        self.current_drives = self.prev_drives
    
    def update(self):
        ret_val = {'attached':{}, 'detached':{}}
        self.prev_drives = self.current_drives
        self.current_drives = DriveStt.get_all_drives()
        attach_diff_set = self.current_drives - self.prev_drives
        if 0 < len(attach_diff_set):
            ret_val['attached'] = attach_diff_set
        detach_diff_set = self.prev_drives - self.current_drives
        if 0 < len(detach_diff_set):
            ret_val['detached'] = detach_diff_set
        return ret_val
