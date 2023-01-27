import os
import sys
import time
import datetime
import shutil
import glob

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.FileDriveStt import DriveStt,FileStt

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
