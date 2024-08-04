import GoogleORTools as got
import Deap_knapsack as dks
import pandas as pd

def main():
    columns_name = ['Case','Total_Value_Deap','Total_Weight_Deap','Is_TimeLimit_Deap','Total_Value_GGoT','Total_Weight_GGoT','Is_TimeLimit_GGoT']
    deap_knapsack = dks.solve_deap()
    ggortool = got.solve_ggorTool()
    #Results are lists of information
    num_case=len(ggortool)
    data=[]
    #Concanating corresponding lists
    for row in range(num_case):
        data.append(deap_knapsack[row] + ggortool[row])
    df=pd.DataFrame(data,columns = columns_name)
    #Result to csv
    df.to_csv('Result.csv')

if __name__ == '__main__':
    main()