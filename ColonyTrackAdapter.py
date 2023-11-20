import subprocess
import os

data_script_path = os.path.join(os.getcwd(), "ColonyTrackFiles", "Scripts", "ColonyTrackScript.r")
metrics_script_path = None

def checkout_data(ct_data_pointer):
    result = subprocess.check_output(["C://Program Files//R//R-4.3.2//bin//x64//rscript", data_script_path], shell=True)

