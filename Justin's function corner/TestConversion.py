import pandas as pd

df = pd.read_csv("your_file.csv", parse_dates=['timestamp_column'])
df.set_index('timestamp_column', inplace=True)

# Resample to 15-minute intervals and take the mean
df_15min = df.resample('15T').mean()
df_15min.reset_index(inplace=True)

# Save or display result
print(df_15min)
