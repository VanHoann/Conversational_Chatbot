import pandas as pd
from tqdm import tqdm

df = pd.read_csv('data/train.csv')
df = df[['conv_id','utterance']]
df['utterance'] = df['utterance'].apply(
    lambda x: x.replace('_comma_',',').lower().strip())
df_out = {'inp': [], 'rep': []}

for conv in tqdm(df['conv_id'].unique(), position=0, total=len(df['conv_id'].unique())):
    # ignore wrong row
    if conv[:4] != 'hit:':
        continue
    temp = df[df['conv_id']==conv]['utterance'].to_list()
    # if conversation only have 1 utterance, skip
    if len(temp) < 1:
        continue
    else:
        for i in range(len(temp)-1):
            df_out['inp'].append(temp[i])
            df_out['rep'].append(temp[i+1])

pd.DataFrame(df_out).to_csv('data/inp_rep.csv', index=False)