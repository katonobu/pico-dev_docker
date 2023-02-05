import os
import sys
import time
import datetime
import shutil
import glob
import serial
from serial.threaded import ReaderThread

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from win.copy_src_config import (src_base_path, src_files)
from lib.FileDriveStt import DriveStt,FileStt
from lib.EnvUtil import EnvUtil
from lib.SerialUtil import (SerialUtil, RxLinesToQueue)

def may_rzpp_drive(drive_to_check):
    ret_val = False
    index_files = glob.glob(drive_to_check + '/INDEX.HTM')
    info_files = glob.glob(drive_to_check + '/INFO_UF2.TXT')
    if drive_to_check+'/INDEX.HTM' in index_files and drive_to_check+'/INFO_UF2.TXT' in info_files:
        print("RZPP Attached {} at {}".format(drive_to_check, datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S')))
        print("------------")
        ret_val = True
    return ret_val

if __name__ == "__main__" :
    import queue

    env = EnvUtil()
    if env.isWindowsOs:
        print("Start : {}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S')))
        print("------------")

        FileStt.set_base_path(src_base_path)
        fileStts = [FileStt(f['file']) for f in src_files]
        driveStt = DriveStt()
        rzpp_drive = None
        for drive in driveStt.get_all_drives():
            if may_rzpp_drive(drive):
                rzpp_drive = drive
        exec_queue = queue.Queue()

        ser_port = SerialUtil.get_probe_serial_name()
        ser = serial.Serial(ser_port, baudrate=115200, timeout=1)
        print("Serial port : {}".format(ser_port))
        with ReaderThread(ser, RxLinesToQueue) as protocol:
            ser_msg_queue = protocol.get_queue()
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
                        if may_rzpp_drive(new_drive):
                            rzpp_drive = new_drive

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
                                        src['func'](act_file, ser_msg_queue)
                                        break
                            # ToDo: Add test here
                            print("done")
                            print("------------")

                # if both updated and rzpp_drive, copy the file to Rzpp
                if rzpp_drive and 0 < len(FileStt.updates):
                    act_file = FileStt.updates.pop()
                    
                    print("Copy to RZPP {} start".format(act_file.split(os.sep)[-1]))
                    shutil.copyfile(act_file, rzpp_drive + os.sep + act_file.split(os.sep)[-1])
                    exec_queue.put(act_file)
                    print("Copy to RZPP finished at {}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S')))
                    print("------------")
                time.sleep(1)
    else:
        print("This script assumes run on Windows.")
