import pandas as pd
from statsmodels.tsa.api import VAR

def time_series(data, future_forcast, location):
    #[[people, violations, time, location],[people, violations, time, location],[people, violations, time, location]]
    columns = ["people", "violations", "time", "location"]

    df = pd.DataFrame(data=data, columns=columns)
    df = df[df["location"]==location]
    df['time'] = pd.to_datetime(df['time'])

    for i in range(len(df)):
        df['time'][i] = df['time'][i].hour

    dict_p = {}
    dict_v = {}
    for i in range(len(df)):
        if(df['time'][i] not in dict_p.keys()):
            dict_p[df['time'][i]] = [df["people"][i]]
        else:
            dict_p[df['time'][i]].append(df["people"][i])
        if (df['time'][i] not in dict_v.keys()):
            dict_v[df['time'][i]] = [df["violations"][i]]
        else:
            dict_v[df['time'][i]].append(df["violations"][i])

    people = []
    violations = []
    times = []

    for k, v in dict_p.items():
        people.append(sum(v) / float(len(v)))
        timet = pd.Timestamp(year=2000, month=1, day=1, hour=k, minute=0, second=0)
        times.append(timet)

    for k, v in dict_v.items():
        violations.append(sum(v) / float(len(v)))

    n_df = pd.DataFrame(columns=["people", "violations", "time"])
    n_df["people"] = people
    n_df["violations"] = violations
    n_df["time"] = times
    n_df = n_df.sort_values(by=['time'])
    n_df.time = pd.DatetimeIndex(n_df.time).to_period('H')
    data1 = n_df[["people", 'violations']]
    data1.index = n_df["time"]
    print(data1)

    model = VAR(data1)
    model_fit = model.fit()
    freq = (n_df["time"][0].hour - n_df["time"][len(n_df)-1].hour) / (len(n_df)-1)
    steps = (future_forcast + n_df["time"][0].hour - n_df["time"][0].hour)/freq
    pred = model_fit.forecast(model_fit.y, steps)
    return pred[0], pred[1]