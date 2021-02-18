import numpy as np
import matplotlib.pyplot as plt

Oi_DTH = [16.7, 18.1, 18.8, 18.7, 20.2, 21.7]
Oi_FTTH = [2.4, 7.6, 8.3, 8.1, 7.8, 8.3]
Vivo_FTTH = [93.6, 88.9, 89.3, 86.9, 78.6, 79.8]
Sky_DTH = [55.6, 58.3, 59.2, 60.9, 61.8, 61.3]
Claro_DTH = [16.2, 15.0, 14.0, 13.3, 12.1, 11.6]
Vivo_DTH = [10.3, 7.5, 6.9, 6.2, 5.4, 4.9]
Claro_TVC = [95.4, 96.0, 96.8, 96.3, 96.4, 96.2]

Oi=[ 8.9, 9.7, 9.9, 9.9, 10.6, 11.0, 11.2, 11.4]
Claro=[49.1, 49.5, 49.7, 49.0, 47.5, 47.2, 47.2, 47.1]
Sky=[30.2, 29.9, 29.9, 30.4, 30.8, 30.7, 30.5, 30.4]

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.025*height,
                f"{int(height)}%",
                ha='center', va='bottom')

#DTH
ax = plt.subplot(1,1,1)
n = np.arange(len(Oi_DTH))
l = ["2018", "2019", "1T20","2T20", "3T20", "4T20"]
b1 = ax.bar(n-0.3, Oi_DTH, width=0.15, color="#41B8D6", align="center")
b2 = ax.bar(n-0.15, Sky_DTH, width=0.15, color="#2C8BB9", align="center")
b3 = ax.bar(n, Claro_DTH, width=0.15, color="#6BE5E8", align="center")
b4 = ax.bar(n+0.15, Vivo_DTH, width=0.15, color="#246466", align="center")
b5 = ax.bar(n+0.3, 100 - np.array(Sky_DTH) - np.array(Oi_DTH) - np.array(Vivo_DTH) - np.array(Claro_DTH),
         width=0.15, color="#1D5C7B", align="center")
ax.set_ylabel("Porcento")
plt.xticks(n,l)
plt.legend(["Oi", "Sky", "Claro", "Vivo", "Outras"])
plt.title("Market Share DTH")
plt.ylim(0,100)
autolabel(b1)
autolabel(b2)
autolabel(b3)
autolabel(b4)
autolabel(b5)
plt.show()

#TVC
ax = plt.subplot(1,1,1)
n = np.arange(len(Oi_DTH))
l = ["2018", "2019", "1T20","2T20", "3T20", "4T20"]
b1 = ax.bar(n-0.2, Claro_TVC, width=0.3, color="#6BE5E8", align="center")
b2 = ax.bar(n+0.2, 100 - np.array(Claro_TVC), width=0.3, color="#1D5C7B", align="center")
ax.set_ylabel("Porcento")
plt.xticks(n,l)
plt.legend(["Claro", "Outras"])
plt.title("Market Share TVC")
plt.yticks([0, 20, 40, 60, 80, 100],[0, 20, 40, 60, 80, 100])
plt.ylim(0,110)
autolabel(b1)
autolabel(b2)
plt.show()

#FTTH
ax = plt.subplot(1,1,1)
n = np.arange(len(Oi_DTH))
l = ["2018", "2019", "1T20","2T20", "3T20", "4T20"]
b1 = ax.bar(n-0.2, Oi_FTTH, width=0.2, color="#41B8D6", align="center")
b2 = ax.bar(n, Vivo_FTTH, width=0.2, color="#246466", align="center")
b3 = ax.bar(n+0.2, 100 - np.array(Oi_FTTH) - np.array(Vivo_FTTH), width=0.2, color="#1D5C7B", align="center")
ax.set_ylabel("Porcento")
plt.xticks(n,l)
plt.legend(["Oi", "Vivo", "Outras"])
plt.title("Market Share FTTH")
plt.yticks([0, 20, 40, 60, 80, 100],[0, 20, 40, 60, 80, 100])
plt.ylim(0,110)
autolabel(b1)
autolabel(b2)
autolabel(b3)
plt.show()

#Market Share
ax = plt.subplot(1,1,1)
n = np.arange(len(Oi))
l = ["2018", "2019", "1T20","2T20", "3T20", "Out/20", "Nov/20", "Dez/20"]
b1 = ax.bar(n-0.3, Claro, width=0.2, color="#6BE5E8", align="center")
b2 = ax.bar(n-0.1, Oi, width=0.2, color="#41B8D6", align="center")
b3 = ax.bar(n+0.1, Sky, width=0.2, color="#2C8BB9", align="center")
b4 = ax.bar(n+0.3, 100 - np.array(Oi)- np.array(Sky)- np.array(Claro), width=0.2, color="#1D5C7B", align="center")
ax.set_ylabel("Porcento")
plt.xticks(n,l)
plt.legend(["Claro", "Oi", "Sky", "Outras"])
plt.title("Market Share Total")
plt.ylim(0,100)
autolabel(b1)
autolabel(b2)
autolabel(b3)
autolabel(b4)
plt.show()