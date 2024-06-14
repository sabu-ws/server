import os
import subprocess
import time
from app import logging as log
# FUNC : scan_yara
def scan_yara(rule_file: str, scan_path: str, quarantine_path: str, log_path: str):

    # LOG FILE
    timestamp = int(time.time())
    log_name = f"yara_{timestamp}.log"
    log_file = os.path.join(log_path, log_name)

    # SCAN
    scan_command = ['yara', '--no-warnings', '--recursive','--no-follow-symlinks', rule_file, scan_path]
    with open(log_file, 'a') as log:
        subprocess.run(scan_command, stdout=log)

    count_all = 0
    # MOVE QUARANTINE
    table_virus = []
    with open(log_file, 'r') as log:
        for line in log.readlines():
            mv_file = line.split(' ', 1)[1].strip()
            if mv_file not in table_virus:
                table_virus.append(mv_file)
                count_all+=1
                os.rename(mv_file, os.path.join(quarantine_path, os.path.basename(mv_file)))

    # LOG NAME
    return f"{log_name};{count_all}"


# MAIN
if __name__ == "__main__":

    rule_file = "sabu-yararules/index.yar"
    scan_path = "DATASET-SB"
    quarantine_path = "quar"
    log_path = "."

    result = scan_yara(rule_file, scan_path, quarantine_path, log_path)
    print(result)
