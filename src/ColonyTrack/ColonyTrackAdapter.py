import subprocess
import os
import rdata


data_script_path = os.path.join(os.getcwd(), os.path.pardir, "ColonyTrackFiles", "Scripts", "ColonyTrackScript.r")
metrics_script_path = None


def checkout_data():
    result = subprocess.check_output(["rscript", data_script_path], shell=True)


def to_df():
    path = os.path.join(os.getcwd(), os.path.pardir, "Data", "ColonyTrackData.RData")
    print(path)
    parsed = rdata.parser.parse_file(rdata.TESTDATA_PATH / path)
    converted = rdata.conversion.convert(parsed)
    print(converted)


