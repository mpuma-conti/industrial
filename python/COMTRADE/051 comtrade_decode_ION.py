import matplotlib.pyplot as plt
import comtrade


#rec = comtrade.load("COMTRADE/cmt00823.cfg", "COMTRADE/cmt00823.dat")
rec = comtrade.load("","COMTRADE/cmt00823.dat")
print("Trigger time = {}s".format(rec.trigger_time))

#plt.figure()
#plt.plot(rec.time, rec.analog[0])
#plt.plot(rec.time, rec.analog[1])
#plt.legend([rec.analog_channel_ids[0], rec.analog_channel_ids[1]])
#plt.show()
df = rec.to_dataframe()
print(df.head())
df.to_csv('archivo.csv')
