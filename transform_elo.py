import numpy as np
import pandas as pd
import datetime

#rawdata = pd.read_csv("data/elo/nfl_elo.csv")
#rawdata.head()

def transform_elo_data(rawdata):
    import pandas as pd
    import datetime
    
    def get_tuesday(x):
        #Gets the tuesday preceeding each week's game- effectively the start of the week
        t = x['date'] + datetime.timedelta(days=(5-x['date'].weekday()))
        if x['date'].weekday()== 0:
            t = t - datetime.timedelta(days=7)
        return t

    mydata = rawdata[rawdata['season'] == max(rawdata['season'])]
    mydata = mydata[mydata['playoff'].isna()]
    mydata = mydata.reset_index()

    keepcols = ['date','season','neutral','team1','team2','elo1_pre','elo2_pre','qbelo1_pre','qbelo2_pre',
                'elo_prob1','elo_prob2','qbelo_prob1','qbelo_prob2','score1','score2']
    mydata = mydata[keepcols]

    mydata['date'] = [datetime.datetime.strptime(d,'%Y-%m-%d') for d in mydata['date']]
    #mydata['wday'] = [d.weekday() for d in mydata['date']]

    mydata['tuesday'] = mydata.apply(lambda x: get_tuesday(x),axis=1)
    mydata['week'] = mydata.groupby('season')['tuesday'].rank("dense")
    mydata['week'] = mydata['week'].astype('int')

    mydata = mydata.drop('tuesday',axis=1)
    mydata = mydata[['date','season','week','team1','team2','elo1_pre','elo2_pre',
                     'elo_prob1','elo_prob2','score1','score2']]

    team1 = mydata[['week','team1','elo_prob1','elo1_pre']]
    team1 = team1.rename(columns={'team1':'team','elo_prob1':'wp','elo1_pre':'elo'})
    team2 = mydata[['week','team2','elo_prob2','elo2_pre']]
    team2 = team2.rename(columns={'team2':'team','elo_prob2':'wp','elo2_pre':'elo'})

    longdata = pd.concat([team1,team2]).drop_duplicates()
    longdata.sort_values(['week','team'])
    
    return longdata
