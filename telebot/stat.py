from datetime import datetime, timezone
from matplotlib import pyplot as plt


class Parsel:
    def __init__(self, subset):
        self.temp = []
        self.hum = []
        self.soil = []
        self.lum1 = []
        self.lum2 = []
        self.ts = []

        for row in subset:
            #print(row)
            self.temp.append(row[0])
            self.hum.append(row[1])
            self.soil.append(row[2])
            self.lum1.append(row[3])
            self.lum2.append(row[4])
            self.ts.append(row[5])


def datetime_to_timestamp(y, m, d, h=0, min_=0, sec=0):
    my_dt = datetime(y, m, d, h, min_, sec)
    my_timestamp = my_dt.replace(tzinfo=timezone.utc).timestamp()
    return int(my_timestamp)


#x = datetime_to_timestamp(2022, 4, 28, 20, 16, 0)
#x = datetime_to_timestamp(2022, 4, 28)
#print(x)


def timestamp_to_datetime(ts):
    objectdate = datetime.fromtimestamp(objtmstmp)


def setup():
    plt.rcParams['axes.grid'] = True
    plt.rcParams["axes.labelsize"] = 22
    
    plt.rcParams["xtick.labelsize"] = 18
    plt.rcParams["ytick.labelsize"] = 18
    
    plt.rcParams["legend.fontsize"] = 20
    plt.rcParams["figure.figsize"]=(14, 4)
    #plt.rcParams["legend.fontsize"] = 22


dateformat_str = "%H:%M\n%d-%m-%y"


def plot_temp_hum(parsel, step=50, n_xticks=12):

    temp_min = parsel.temp[::step]
    hum_min = parsel.hum[::step]
    ts_min = parsel.ts[::step]
    ts_min = [datetime.fromtimestamp(elem).strftime(dateformat_str) for elem in ts_min]

    plt.plot(ts_min, temp_min, label='temp')
    plt.plot(ts_min, hum_min, label='hum')
    plt.draw()
    plt.xticks(rotation="vertical")
    
    
    N = int( len(temp_min)/n_xticks ) + 1  # 1 tick every 3
    print("Plot every ",N , "th xtick")
    
    xticks_pos, xticks_labels = plt.xticks()  # get all axis ticks
    myticks = [j for i,j in enumerate(xticks_pos) if not i%N]  # index of selected ticks
    newlabels = [label for i,label in enumerate(xticks_labels) if not i%N]
    plt.xticks(myticks, newlabels)  # set new X axis ticks and labels
    # plt.yticks(fontsize=14)
    
    plt.legend()
    plt.savefig('1.jpg')
    plt.show()
    return


def plot_soil(parsel, step=50, n_xticks=12):
    soil_min = parsel.soil[::step]
    ts_min = parsel.ts[::step]
    ts_min = [datetime.fromtimestamp(elem).strftime(dateformat_str) for elem in ts_min]
    
    plt.plot(ts_min, soil_min, label='Soil')
    plt.draw()
    plt.xticks(rotation="vertical")
    
    N = int( len(soil_min)/n_xticks ) + 1
    print("Plot every ",N , "th xtick")
    
    xticks_pos, xticks_labels = plt.xticks()  # get all axis ticks
    myticks = [j for i,j in enumerate(xticks_pos) if not i%N]  # index of selected ticks
    newlabels = [label for i,label in enumerate(xticks_labels) if not i%N]
    plt.xticks(myticks, newlabels)  # set new X axis ticks and labels
    
    #plt.scatter(ts_min, soil_min, label='Soil')
    plt.legend()
    plt.savefig('2.jpg')
    plt.show()
    return


def plot_lum(parsel, step=50, n_xticks=12):

    lum1_min = parsel.lum1[::step]
    lum2_min = parsel.lum2[::step]

    ts_min = parsel.ts[::step]
    ts_min = [datetime.fromtimestamp(elem).strftime(dateformat_str) for elem in ts_min]
    #ts_min = list(map(datetime.fromtimestamp(elem).strftime("%H:%M"), ts_min ))

    plt.plot(ts_min, lum1_min, label='Luminance left')
    plt.plot(ts_min, lum2_min, label='Luminance right')
    plt.draw()
    plt.xticks(rotation="vertical")
    #plt.locator_params(axis='x', nbins=10)
    
    N = int( len(lum1_min)/n_xticks ) + 1  # 1 tick every 3
    print("Plot every ",N , "th xtick")
    
    xticks_pos, xticks_labels = plt.xticks()  # get all axis ticks
    myticks = [j for i,j in enumerate(xticks_pos) if not i%N]  # index of selected ticks
    newlabels = [label for i,label in enumerate(xticks_labels) if not i%N]
    plt.xticks(myticks, newlabels)  # set new X axis ticks and labels
    
    plt.legend()
    plt.savefig('3.jpg')
    plt.show()
    return


