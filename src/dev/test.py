import pandas as pd
df = pd.DataFrame({'time': ['2022-7-16 11:05:00',
                               '2025-7-18 12:00:30']})
print(df)
df['time'] = pd.to_datetime(df['time'])
print(type(df))