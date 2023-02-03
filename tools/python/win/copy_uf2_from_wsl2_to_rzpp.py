import os
import sys
import time
import datetime
import shutil
import glob

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from win.copy_src_config import (src_base_path, src_files)
from lib.FileDriveStt import DriveStt,FileStt
from lib.EnvUtil import EnvUtil

if __name__ == "__main__" :
    import queue

    env = EnvUtil()
    if env.isWindowsOs:
        FileStt.set_base_path(src_base_path)
        fileStts = [FileStt(f['file']) for f in src_files]

        driveStt = DriveStt()

        rzpp_drive = None

        exec_queue = queue.Queue()

        print("Start : {}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S')))
        print("------------")
        while True:
            # Watch file is updated.
            for fileStt in fileStts:
                if fileStt.update():
                    fileStt.print()
                    print("------------")

            # Watch Local Drive
            drives_diff = driveStt.update()

            # if attached and it has '/INDEX.HTM' and '/INFO_UF2.TXT', the drive letter is set to `rzpp_drive`
            if 0 < len(drives_diff['attached']):
                for new_drive in drives_diff['attached']:
                    files = glob.glob(new_drive + '/**', recursive=True)
                    if new_drive+'/INDEX.HTM' in files and new_drive+'/INFO_UF2.TXT' in files:
                        rzpp_drive = new_drive
                        print("RZPP Attached {}".format(drives_diff['attached']))
                        print("------------")

            # if detached 'rzpp_drive', None is set to `rzpp_drive` and run test.
            if 0 < len(drives_diff['detached']):
                for det_drive in drives_diff['detached']:
                    if det_drive == rzpp_drive:
                        rzpp_drive = None
                        print("RZPP Detached {}".format(det_drive))
                        print("Run test ....")
                        if not exec_queue.empty():
                            act_file = exec_queue.get()
                            for src in src_files:
                                if src['file'].split(os.sep)[-1] == act_file.split(os.sep)[-1]:
                                    src['func'](act_file)
                                    break
                        # ToDo: Add test here
                        print("done")
                        print("------------")

            # if both updated and rzpp_drive, copy the file to Rzpp
            if rzpp_drive and 0 < len(FileStt.updates):
                act_file = FileStt.updates.pop()
                
                print("Copy to RZPP {} start".format(act_file.split(os.sep)[-1]))
                shutil.copyfile(act_file, new_drive + os.sep + act_file.split(os.sep)[-1])
                exec_queue.put(act_file)
                print("Copy to RZPP finished")
                print("------------")
            time.sleep(1)
    else:
        print("This script assumes run on Windows.")
