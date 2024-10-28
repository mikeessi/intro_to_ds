import pandas as pd
import statsmodels.api as sm
from copy import deepcopy


PATH = "candidates/parhaat/"

df = pd.read_json(PATH+"candidate_236.json",lines=True)
res = df.drop([0,1,2,3,4,5,7,9,11,13,14,15,17])                  ### MUUTA TÄMÄ
print(res)


def predictYears(df):

    latest = df["Vuosi"].iloc[-1]
    yrs = [latest+1,latest+2,latest+3]
    start = df["Vuosi"].size-1
    end = start+2
    df.reset_index(inplace=True)

    model = sm.tsa.arima.ARIMA(df["Alin pistemäärä"],order=(1,0,0))
    fitted_model = model.fit()

    preds = fitted_model.predict(start=start,end=end)

    pairs = [(yrs[i],float(round(preds.iloc[i],2))) for i in range(len(yrs))]

    d = df[["Yliopisto","Vuosi","Ala","Alin pistemäärä"]] 

    dfd = d.to_dict(orient="index")

    last = list(dfd.keys())[-1]

    i = last+1
    for pair in pairs:
        dfd[i] = deepcopy(dfd[last])
        dfd[i]["Vuosi"] = pair[0]
        dfd[i]["Alin pistemäärä"] = pair[1]
        i += 1
    
    output =  pd.DataFrame.from_dict(dfd,orient="index")

    return output


def toJSON(df,name):
    df.to_json(f"ready/{name}.json",orient="records",lines=True)
    print("done")

toJSON(predictYears(res),"40")

