from collections import OrderedDict as od
import pandas as pd
class Analyse_Result_File():
    def __init__(self, columns, result_csv, args):
        self.dict = columns
        self.result_stats=r'{}'.format(result_csv)+'_stats.csv'
        self.result_failures=r'{}'.format(result_csv)+'_failures.csv'
        self.df = pd.read_csv(self.result_stats)
        self.args=args
        index=list(self.df['Type']).index(self.args.Api_Method)
        self.dict['URL'].append('https://'+args.Server)
        self.dict['Method'].append(args.Api_Method)
        self.dict['Success Rate'].append(self.get_Success_Rate(index=index))
        percentiles = self.get_Latencies(index=index)
        for i in percentiles:
            self.dict[i].append(percentiles[i])
        self.dict['Test Runtime'].append(args.Run_Time)
        self.dict['Requests sent'].append(self.df['Request Count'][index])
        self.dict['Bottle Neck'].append('Yes' if self.check_Latencies(index=index) is False else 'No')
        self.dict['response_codes(client exptd_response_count)'].append(self.get_Response_Codes(self.result_stats,self.result_failures,index=index))

    def get_Latencies(self,index):
        """
        This method returns the Latency metrics for .50, .90 and .99 percentiles from dataframe(csv file)
           """
        percentiles = {}
        percentiles["e2e_0.50(ms)"] = round(self.df['50%'][index],0)
        percentiles["e2e_0.90(ms)"] = round(self.df['90%'][index], 0)
        percentiles["e2e_0.99(ms)"] = round(self.df['99%'][index], 0)
        return percentiles

    def check_Latencies(self,index):
        """
        This method reads the Latency metrics for .50, .90 and .99 percentiles from dataframe(csv file) and compares them with given threshold values
        :return: True or False
            """
        e2e_50_th, e2e_90_th, e2e_99_th = self.args.E2e_50_threshold, self.args.E2e_90_threshold, self.args.E2e_99_threshold
        e2e_50 = round(self.df['50%'][index], 0)
        e2e_90 = round(self.df['90%'][index], 0)
        e2e_99 = round(self.df['99%'][index], 0)
        return True if ((e2e_50 <= e2e_50_th) and (e2e_90 <= e2e_90_th) and (e2e_99 <= e2e_99_th)) else False

    def get_Success_Rate(self,index):
        """
        This method returns the percentage of threads whose requests succeeded, from dataframe(csv file)
            """
        Success_Rate = round(((self.df['Request Count'][index]) - self.df['Failure Count'][index]) / (self.df['Request Count'][index]), 2)
        Success_Rate = str(Success_Rate * 100) + '%'
        return Success_Rate
    
    def get_Response_Codes(self,stats,failures,index):
        """
        This method returns the various response codes obtained during the load test, from csvfiles
            """
        df1 = pd.read_csv(stats)
        df2 = pd.read_csv(failures)
        d = od()
        d[200] = df1['Request Count'][index] - df1['Failure Count'][index]
        if(len(df2)>0):
            for i in range(len(df2)):
                s2 = df2['Error'][i].split(' ')
                d[s2[0]] = df2['Occurrences'][i]
        l = []
        for i in d:
            l.append('{ ' + str(i) + " : " + str(d[i]) + " }")
        s = ', '.join(l)
        return s
    def get_Result(self):
        """
         This method returns the aggregate results of the load test performed, from dataframe(csv file)
            """
        return self.dict

if __name__ == "__main__":
    pass