import os
import time
import datetime
import shutil
import glob

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
        self.current_drives = set([f'{d}:' for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f'{d}:')])
        attach_diff_set = self.current_drives - self.prev_drives
        if 0 < len(attach_diff_set):
            ret_val['attached'] = attach_diff_set
        detach_diff_set = self.prev_drives - self.current_drives
        if 0 < len(detach_diff_set):
            ret_val['detached'] = detach_diff_set
        return ret_val



if __name__ == "__main__" :
    import queue

    def dummy(hoge):
        print("---- {} ----".format(hoge))

    src_base_path = os.sep.join([os.path.dirname(__file__), 'uf2'])
    src_files = [
        {
            'file':'picow_freertos_ping_sys.uf2',
            'func':dummy
        },{
            'file':'http_server.uf2',
            'func':dummy
        },{
            'file':'ping.uf2',
            'func':dummy
        }
    ]

    FileStt.set_base_path(src_base_path)
    fileStts = [FileStt(f['file']) for f in src_files]

    driveStt = DriveStt()

    rzpp_drive = None

    exec_queue = queue.Queue()

    print("Start : {}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S')))
    while True:
        # Watch file is updated.
        for fileStt in fileStts:
            if fileStt.update():
                fileStt.print()
                print("------------")

        # Watch Loca Drive
        drives_diff = driveStt.update()

        # if attached and it has '/INDEX.HTM' and '/INFO_UF2.TXT', the drive letter is set to `rzpp_drive`
        if 0 < len(drives_diff['attached']):
            for new_drive in drives_diff['attached']:
                files = glob.glob(new_drive + '/**', recursive=True)
                if new_drive+'/INDEX.HTM' in files and new_drive+'/INFO_UF2.TXT' in files:
                    rzpp_drive = new_drive
                    print("RZPP Attached {}".format(drives_diff['attached']))

        # if detached 'rzpp_drive', None is set to `rzpp_drive` and run test.
        if 0 < len(drives_diff['detached']):
            for det_drive in drives_diff['detached']:
                if det_drive == rzpp_drive:
                    rzpp_drive = None
                    print("RZPP Detached {}".format(det_drive))
                    print("Run test ....")
                    if not exec_queue.empty():
                        act_file = exec_queue.get()
                        print(act_file)
                        for src in src_files:
                            if src['file'] == act_file.split(os.sep)[-1]:
                                src['func'](act_file)
                                break
                    # ToDo: Add test here
                    print("done")

        # if both updated and rzpp_drive, copy the file to Rzpp
        if rzpp_drive and 0 < len(FileStt.updates):
            act_file = FileStt.updates.pop()
            
            print("Copy to RZPP start")
            shutil.copyfile(act_file, new_drive + os.sep + act_file.split(os.sep)[-1])
            exec_queue.put(act_file)
            print("Copy to RZPP finished")
            print("------------")
        time.sleep(1)
