import os, sys
sys.path.append(os.getcwd())
from collections import OrderedDict
import Analyse
import pandas as pd
import subprocess, argparse
from pathlib import Path


def Run_test(Locust_file, ARGS, result_file, ):
    subprocess.call(
        r'locust -f {} --host {} --headless -u {} -r {} -t {} --csv={}'.format(Locust_file, 'https://' + ARGS.Server,
                                                                               ARGS.No_of_Users, ARGS.Hatch_Rate,
                                                                               ARGS.Run_Time, result_file), shell=True)
    analyser = Analyse.Analyse_Result_File(columns=columns, result_csv=result_file, args=ARGS)
    return analyser.get_Result()


if __name__ == "__main__":
    columns = OrderedDict()
    st = ['URL', 'Method', 'Success Rate', "e2e_0.50(ms)", "e2e_0.90(ms)", "e2e_0.99(ms)", 'Bottle Neck',
          'Test Runtime', 'Requests sent',
          'response_codes(client exptd_response_count)']
    for i in st:
        columns[i] = []
    # below argparse for argument to be passed as input for details
    PARSER = argparse.ArgumentParser(description='PNS build execution.')
    PARSER.add_argument('-No_of_Users', type=int, required=True, help='Starting value to perform test')
    PARSER.add_argument('-Hatch_Rate', type=int, required=True, help='Step value')
    PARSER.add_argument('-E2e_50_threshold', type=int, required=True, help='e2e .50 threshold ms')
    PARSER.add_argument('-E2e_90_threshold', type=int, required=True, help='e2e .90 threshold ms')
    PARSER.add_argument('-E2e_99_threshold', type=int, required=True, help='e2e .99 threshold ms')
    PARSER.add_argument('-Server', type=str, required=True, help='Server to test')
    PARSER.add_argument('-Api_Method', type=str, required=True, help='path to test')
    PARSER.add_argument('-Run_Time', type=str, required=True, help='Specified time for which Locust will run')
    ARGS = PARSER.parse_args()
    (No_of_Users, Hatch_Rate, Run_Time) = (ARGS.No_of_Users, ARGS.Hatch_Rate, ARGS.Run_Time)
    base = Path(__file__)
    Locust_file = r'{}'.format(str((base / "../Locust_files/locustfile.py").resolve()))
    result_file = r'{}'.format(str((base / "../Data/CSV/testoutput").resolve()))
    Aggregate_file = r'{}'.format(str((base / "../Data/CSV/Aggregate_Result.csv").resolve()))
    print('Lfile:',Locust_file,'rfile:',result_file,'Afile:',Aggregate_file)
    data = Run_test(Locust_file=Locust_file, ARGS=ARGS, result_file=result_file)
    df = pd.DataFrame(data)
    df.to_csv(r'{}'.format(Aggregate_file), index=False)
