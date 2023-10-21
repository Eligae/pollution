import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('AirPollutionAVG.csv')
plt.figure(figsize=(6, 6)) 
plt.plot(df["date"], df["일산화탄소(CO)"], label="CO")
plt.plot(df["date"], df["염화수소(HCl)"], label="HCl")
plt.plot(df["date"], df["황산화물(SO2)"], label="SO2")
plt.plot(df["date"], df["먼지(Dust)"], label="Dust")
plt.plot(df["date"], df["질소산화물(NOx)"], label="NOx")


plt.title("Air Pollution Graph")
plt.xlabel("Date")
plt.ylabel("ppm")
plt.legend() 

x_ticks = df["date"].iloc[::5]
plt.xticks(x_ticks, rotation=45)

plt.tight_layout()
plt.savefig("Air_Pollution_Graph.png")
