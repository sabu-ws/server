import os
import subprocess
import time

# FUNC : scan_oletools
def scan_oletools(scan_path: str, quarantine_path: str, log_path: str):

    # LOG FILE
    timestamp = int(time.time())
    log_name = f"oletools_{timestamp}.log"
    log_file = os.path.join(log_path, log_name)

    # SCAN
    with open(log_file, "w") as log:
            for root, dirs, files in os.walk(scan_path):
                for file in files:

                    fp = root+"/"+file

                    scan_command = ['oleid', fp]
                    output_command = subprocess.Popen(scan_command, stdout=subprocess.PIPE).communicate()[0].decode()
                    output_lines = output_command.split("\n")

                    for i in output_lines:
                        if "Container type" in i and "|OLE" in i:

                            for i in output_lines:
                                if "VBA Macros" in i and "|Yes, suspicious" in i:

                                    print("[MALICIOUS] " + fp)
                                    log.write("[MALICIOUS] " + fp + '\n')

    # MOVE QUARANTINE
    with open(log_file, 'r') as log:
        for line in log:
            try:
                mv_file = line.split(' ', 1)[1].strip()
                file = os.path.join(quarantine_path, os.path.basename(mv_file))
                check_file = os.path.isfile(file)

                if check_file is True:
                    mv_file_dupl = mv_file + "_duplicated"
                    os.rename(mv_file, os.path.join(quarantine_path, os.path.basename(mv_file_dupl)))
                
                else:
                    os.rename(mv_file, os.path.join(quarantine_path, os.path.basename(mv_file)))

            except Exception as e:
                print(f"Error move {mv_file} : {e}")

    # LOG NAME
    return f"{log_name}"


# MAIN
if __name__ == "__main__":

    scan_path = "DATASET-SB"
    quarantine_path = "quar"
    log_path = "."

    result = scan_oletools(scan_path, quarantine_path, log_path)
    print(result)
