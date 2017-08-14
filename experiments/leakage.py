__author__ = 'shaleen'
from matplotlib import rc_file
rc_file('matplotlibrc-singlecolumn')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 3.5, 1.95
#averaged on 3 33 runs. max and min calculated separately. summarised runs below
randomdprimeprice = [[0.3003003003003003, 0.0, 0.7007007007007007, 0.0, 0.0, 0.1001001001001001, 1.5015015015015014, 0.3003003003003003, 1.7017017017017018, 32.632632632632635      , 0.1001001001001001, 4.804804804804805, 5.804904904904905, 0.7007007007007007, 0.2002002002002002, 0.6006006006006006, 0.0, 1.2012012012012012, 0.2002002002002002, 0.6006006006006006    , 0.0, 29.62962962962963, 0.0, 0.0, 16.716716716716718, 4.104104104104104, 0.3003003003003003, 0.0, 0.1001001001001001, 0.7007007007007007, 0.0, 6.506506506506507, 2.6026026026026026, 64.96496496496496],
                     [0.5991977963949902, 0.0, 1.395790184578971, 0.0, 0.0, 0.19999979959940406, 2.9785541297052798, 0.5993981969957929, 3.372140909678445, 54.5837128419711, 0.19999979959940406, 9.373938503067636, 9.564319073828587, 1.395790184578971, 0.3997991985979943, 1.1969927885843834, 0.0, 2.386771155539924, 0.39959879799719156, 1.1969927885843834, 0.0, 50.44984924864805, 0.0, 0.0, 30.622213805396992, 8.03566329091855, 0.5993981969957929, 0.0, 0.19999979959940406, 1.395188982776574, 0.0, 12.58315372429486, 5.134864594324052, 87.65983200417635], [0.32362250410845617, 0.0, 0.8017959417645715, 0.0, 0.0, 0.11458591672907081, 1.6770739304392324, 0.34371416926287646, 1.8857006057574788, 36.485490815304225, 0.11458591672907081, 5.4834852750428205, 5.597357176114093, 0.8017959417645715, 0.2291573113386458, 0.6872973768261459, 0.0, 1.3740693218324385, 0.20906564618422552, 0.6872973768261459, 0.0, 33.14961775869361, 0.0, 0.0, 18.922437546303804, 4.685956146501901, 0.34371416926287646, 0.0, 0.11458591672907081, 0.7540291379943609, 0.0, 7.417221782185379, 2.9744758318287157, 70.22491683809142], [15.90634565547838, 0.0, 28.174015314267027, 0.0, 0.0, 0.0, 39.20872085214085, 15.90634565547838, 41.02090540140172, 83.78605534477988, 0.0, 56.049492634011976, 56.348030628534055, 28.174015314267027, 10.035786744633397, 25.942132400111777, 0.0, 35.97791914474517, 10.035786744633397, 25.942132400111777, 0.0, 82.38832326746504, 0.0, 0.0, 74.1012816647038, 53.76724939163025, 15.90634565547838, 0.0, 0.0, 28.174015314267027, 0.0, 60.43919906929778, 47.17261061726872, 93.7550691204812]],\
                    [[0.3003003003003003, 0.0, 0.9009009009009009, 0.0, 0.0, 0.2002002002002002, 0.8008008008008008, 0.3003003003003003, 0.8008008008008008, 33.532832832832835, 0.2002002002002002, 5.6057057057057055, 5.704704704704705, 0.5005005005005005, 0.5005005005005005, 0.5005005005005005, 0.0, 0.8008008008008008, 0.0, 1.4014014014014013,         0.0, 30.73173173173173, 0.0, 0.0, 15.114114114114114, 3.2032032032032034, 0.2002002002002002, 0.0, 0.2002002002002002, 1.2012012012012012, 0.0, 8.308308308308309, 3.2032032032032034, 66.86686686686687],
                     [0.5987969951933958, 0.0, 1.7927837747657605, 0.0, 0.0, 0.39959879799719156, 2.5943871799727671, 0.5991977963949902, 3.5941867793719644, 54.85285084884685, 0.3997991985979943, 11.08014921828736, 9.183357531705882, 0.9979949919889819, 0.9979949919889819, 0.9979949919889819, 0.0, 1.5943871799727671, 0.0, 2.781760739718697, 0.0, 53.362671981290596, 0.0, 0.0, 26.222017813609412, 6.3005948891834755, 0.3997991985979943, 0.0, 0.3997991985979943, 2.386771155539924, 0.0, 15.917819721623527, 6.3005948891834755, 88.95482068655241], [0.29594736549266587, 0.0, 1.0307492270339447, 0.0, 0.0, 0.20906564618422552, 0.916279896748029, 0.32362250410845617, 0.8961882315936087, 36.703184246970245, 0.2291573113386458, 6.507781818752656, 5.369598134144516, 0.5727842166457497, 0.5727842166457497, 0.5727842166457497, 0.0, 0.916279896748029, 0.0, 1.6028759899173628, 0.0, 35.50480805875289, 0.0, 0.0, 16.006116405587314, 3.6594730477114368, 0.2291573113386458, 0.0, 0.2291573113386458, 1.3740693218324385, 0.0, 9.43972587822267, 3.6594730477114368, 72.14594480976695], [15.90634565547838, 0.0, 31.81269131095676, 0.0, 0.0, 10.035786744633397, 30.10736023390019, 15.90634565547838, 30.10736023390019, 83.87460962553044, 10.035786744633397, 58.53764028705903, 55.74466916955488, 23.302375196662467, 23.302375196662467, 23.302375196662467, 0.0, 30.10736023390019, 0.0, 38.209802058900415, 0.0, 83.38071870859335, 0.0, 0.0, 71.65101482503326, 50.178933723166985, 10.035786744633397, 0.0, 10.035786744633397, 35.97791914474517, 0.0, 63.978536221626705, 50.178933723166985, 94.1728551539706]], \
                    [[0.4004004004004004, 0.0, 0.8008008008008008, 0.0, 0.0, 0.3003003003003003, 0.9009009009009009, 0.5005005005005005, 1.4014014014014013, 32.632132132132135, 0.3003003003003003, 5.506506506506507, 5.003003003003003, 0.7007007007007007, 0.4004004004004004, 0.4004004004004004, 0.0, 1.3013013013013013, 0.0, 1.001001001001001,         0.0, 30.63163163163163, 0.0, 0.0, 16.81781781781782, 4.804804804804805, 0.0, 0.0, 0.2002002002002002, 0.5005005005005005, 0.0, 7.5075075075075075, 3.003003003003003, 65.16516516516516],
                     [0.7983959935911833, 0.0, 1.5943871799727671, 0.0, 0.0, 0.5991977963949902, 2.7927837747657605, 0.9979949919889819, 3.7813599385170917, 53.907360814267726, 0.5993981969957929, 12.58315372429486, 9.912819726633545, 1.395790184578971, 0.7987967947927888, 0.7987967947927888, 0.0, 2.5843661479297064, 0.0, 1.9907795683571483, 0.0, 53.22499676854031, 0.0, 0.0, 32.44305366427489, 9.373738102466833, 0.0, 0.0, 0.3997991985979943, 0.9979949919889819, 0.0, 14.443472501530563, 5.912819726633545, 87.79830881932983], [0.4180731455978859, 0.0, 0.916279896748029, 0.0, 0.0, 0.32362250410845617, 1.0307492270339447, 0.5727842166457497, 1.5626926596085222, 35.940880930525765, 0.34371416926287646, 7.417221782185379, 3.431200428309833, 0.8017959417645715, 0.45825647590672647, 0.45825647590672647, 0.0, 1.4884800053045932, 0.0, 1.125112252695415, 0.0, 35.29527830979039, 0.0, 0.0, 20.15274171545549, 5.463393609888401, 0.0, 0.0, 0.2291573113386458, 0.5727842166457497, 0.0, 8.512440838100177, 3.431200428309833, 70.30306892089556], [20.071573489266793, 0.0, 30.10736023390019, 0.0, 0.0, 15.90634565547838, 31.81269131095676, 23.302375196662467, 38.209802058900415, 83.56227067698666, 15.90634565547838, 60.43919906929778, 49.24450759677425, 28.174015314267027, 20.071573489266793, 20.071573489266793, 0.0, 37.13682387263532, 0.0, 33.338161941295866, 0.0, 83.33497276289778, 0.0, 0.0, 75.02486647290532, 56.049492634011976, 0.0, 0.0, 10.035786744633397, 23.302375196662467, 0.0, 62.51109604880332, 49.24450759677425, 93.79961863183767]]

actualprice = [[0.3003003003003003, 0.0, 0.901901901901902, 0.0, 0.0, 0.3003003003003003, 1.002002002002002, 1.1021021021021022, 1.901901901901902, 33.833833833833836,      0.4004004004004004, 5.505505505505505, 5.506506506506507, 1.3013013013013013, 1.001001001001001, 0.6006006006006006, 0.0, 1.001001001001001, 0.0, 0.5005005005005005   , 0.0, 29.324324324324323, 0.0, 0.0, 16.316316316316318, 3.4034034034034035, 0.1001001001001001, 0.1001001001001001, 0.2002002002002002, 0.6006006006006006, 0.0, 7.007007007007007, 2.8028028028028027, 66.26826826826827],
               [0.5991977963949902, 0.0, 1.86572768965161, 0.0, 0.0, 0.4991977963949902, 2.9619198778357956, 0.757911665419178, 3.7653268884500157, 54.1865168471775, 0.3987967947927888, 10.702193685176663, 12.58315372429486, 2.5843661479297064, 1.990979968957951, 1.1969927885843834, 0.0, 1.990979968957951, 0.0, 0.9979949919889819, 0.0   , 53.70677083489897, 0.0, 0.0, 29.95407820232645, 6.687568449330206, 0.19999979959940406, 0.19999979959940406, 0.3997991985979943, 1.1969927885843834, 0.0, 13.51601852102352, 5.524242961680404, 89.86143300457616],
               [0.32362250410845617, 0.0, 2.1746349067326753, 0.0, 0.0, 0.32362250410845617, 2.288942383747694, 2.4032350568042093, 2.1344515764238348, 37.79035026144663, 0.45825647590672647, 6.26017598029891, 7.417221782185379, 1.4884800053045932, 1.1452039178498352, 0.6872973768261459, 0.0, 1.1452039178498352, 0.0, 0.5727842166457497  , 0.0, 27.29775437832471, 0.0, 0.0, 18.474530147928505, 3.887685716407041, 0.11458591672907081, 0.11458591672907081, 0.2291573113386458, 0.6872973768261459, 0.0, 7.9851179852919785, 3.2028679819397055, 73.42130403247278],
               [15.90634565547838, 0.0, 42.63129463158064, 0.0, 0.0, 15.90634565547838, 43.373948685929264, 44.08036096974541, 42.63129463158064, 84.30943448990405, 20.071573489266793, 58.020493178948314, 60.43919906929778, 37.13682387263532, 33.338161941295866, 25.942132400111777, 0.0, 33.338161941295866, 0.0, 23.302375196662467, 0.0   , 79.5317282773919, 0.0, 0.0, 73.7502686001465, 51.05669214603512, 0.0, 0.0, 10.035786744633397, 25.942132400111777, 0.0, 61.51217725556289, 48.24558880353381, 94.47316238901153]]

def maxrandprice():
    ret_arr = []
    arr = []
    for j in range(0,4):
        arr = []
        for k in range(0,34):
            arr.append(max(math.fabs(randomdprimeprice[0][j][k] - actualprice[j][k]), math.fabs(randomdprimeprice[1][j][k] - actualprice[j][k]),
                           math.fabs(randomdprimeprice[2][j][k] - actualprice[j][k])))
        ret_arr.append(arr)
    return ret_arr

def minrandprice():
    ret_arr = []
    arr = []
    for j in range(0,4):
        arr = []
        for k in range(0,34):
            arr.append(min(math.fabs(randomdprimeprice[0][j][k] - actualprice[j][k]), math.fabs(randomdprimeprice[1][j][k] - actualprice[j][k]),
                           math.fabs(randomdprimeprice[2][j][k] - actualprice[j][k])))
        ret_arr.append(arr)
    return ret_arr

def avgrandprice():
    ret_arr = []
    arr = []
    for j in range(0,4):
        arr = []
        for k in range(0,34):
            arr.append(math.fabs((randomdprimeprice[0][j][k]+randomdprimeprice[1][j][k]+randomdprimeprice[2][j][k])/3.0 - actualprice[j][k]))
        ret_arr.append(arr)
    return ret_arr

def leakagedis():
    fig, ax = plt.subplots()
    ax.set_ylim([0, 1000])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 11, 5))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks(np.arange(1, 34, 5))
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.2)
    ax.tick_params(
            axis='x',          # changes apply to the x-axis
            which='major',      # both major and minor ticks are affected
            bottom='on',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            direction='out',
            labelbottom='on') # labels along the bottom edge are off

    ax.tick_params(
            axis='y',
            which='major',
            left='on',
            right='off',
            direction='out')

    percentavg = []
    for i in range(0, 34):
        if avgrandprice()[0][i] == 0:
            percentavg.append(0)
        else:
            percentavg.append(avgrandprice()[0][i]*100/avgrandprice()[0][i])
    percentmax = []
    for i in range(0, 34):
        if avgrandprice()[0][i] == 0:
            percentmax.append(0)
        else:
            percentmax.append(maxrandprice()[0][i]*100/avgrandprice()[0][i])
    percentmin = []
    for i in range(0, 34):
        if avgrandprice()[0][i] == 0:
            percentmin.append(0)
        else:
            percentmin.append(avgrandprice()[0][i]*100/avgrandprice()[0][i])

    ax.plot([x for x in range(1,35)], percentavg, color='b', marker='x', markersize=2)
    ax.plot([x for x in range(1,35)], percentmax, color='r', marker='s', markersize=2)
    ax.plot([x for x in range(1,35)], percentmin, color='g', marker='^', markersize=2)
    #ax.plot([x for x in range(1,35)], [y for y in pricesel[1][:9]], color='r', marker='s', markersize=2)
    plt.ylabel("Percentage")
    plt.grid(True)
    plt.xlabel("Query")
    lgd = plt.legend(['Average', 'Maximum', 'Minimum'], loc='upper left', ncol=1, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/paper/cs799_summer16.git/trunk/experiments/benchmarkleakagedisagreementpercent', bbox_extra_artists=(lgd,), bbox_inches='tight')
def leakagetsa():
    fig, ax = plt.subplots()
    ax.set_ylim([0, 10])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 10, 1))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks(np.arange(1, 34, 5))
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.2)
    ax.tick_params(
            axis='x',          # changes apply to the x-axis
            which='major',      # both major and minor ticks are affected
            bottom='on',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            direction='out',
            labelbottom='on') # labels along the bottom edge are off

    ax.tick_params(
            axis='y',
            which='major',
            left='on',
            right='off',
            direction='out')



    ax.plot([x for x in range(1,35)], [avgrandprice()[1][y]  for y in range(0,34)], color='b', marker='x', markersize=2)
    ax.plot([x for x in range(1,35)], [maxrandprice()[1][y]  for y in range(0,34)], color='r', marker='s', markersize=2)
    ax.plot([x for x in range(1,35)], [minrandprice()[1][y]  for y in range(0,34)], color='g', marker='^', markersize=2)
    #ax.plot([x for x in range(1,35)], [y for y in pricesel[1][:9]], color='r', marker='s', markersize=2)
    plt.ylabel("Price difference out of 100")
    plt.grid(True)
    plt.xlabel("Query")
    lgd = plt.legend(['Average', 'Maximum', 'Minimum'], loc='lower left', ncol=2, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/benchmarkleakagetsa', bbox_extra_artists=(lgd,), bbox_inches='tight')

def leakagebuc():
    fig, ax = plt.subplots()
    ax.set_ylim([0, 10])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 10, 1))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks(np.arange(1, 34, 5))
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.2)
    ax.tick_params(
            axis='x',          # changes apply to the x-axis
            which='major',      # both major and minor ticks are affected
            bottom='on',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            direction='out',
            labelbottom='on') # labels along the bottom edge are off

    ax.tick_params(
            axis='y',
            which='major',
            left='on',
            right='off',
            direction='out')



    ax.plot([x for x in range(1,35)], [avgrandprice()[2][y]  for y in range(0,34)], color='b', marker='x', markersize=2)
    ax.plot([x for x in range(1,35)], [maxrandprice()[2][y]  for y in range(0,34)], color='r', marker='s', markersize=2)
    ax.plot([x for x in range(1,35)], [minrandprice()[2][y]  for y in range(0,34)], color='g', marker='^', markersize=2)
    #ax.plot([x for x in range(1,35)], [y for y in pricesel[1][:9]], color='r', marker='s', markersize=2)
    plt.ylabel("Price out of 100")
    plt.grid(True)
    plt.xlabel("Query")
    lgd = plt.legend(['Average', 'Maximum', 'Minimum'], loc='lower left', ncol=2, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/benchmarkleakagebucket', bbox_extra_artists=(lgd,), bbox_inches='tight')
def leakageaps():
    fig, ax = plt.subplots()
    ax.set_ylim([0, 50])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 50, 5))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks(np.arange(1, 34, 5))
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.2)
    ax.tick_params(
            axis='x',          # changes apply to the x-axis
            which='major',      # both major and minor ticks are affected
            bottom='on',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            direction='out',
            labelbottom='on') # labels along the bottom edge are off

    ax.tick_params(
            axis='y',
            which='major',
            left='on',
            right='off',
            direction='out')



    ax.plot([x for x in range(1,35)], [avgrandprice()[3][y]  for y in range(0,34)], color='b', marker='x', markersize=2)
    ax.plot([x for x in range(1,35)], [maxrandprice()[3][y]  for y in range(0,34)], color='r', marker='s', markersize=2)
    ax.plot([x for x in range(1,35)], [minrandprice()[3][y]  for y in range(0,34)], color='g', marker='^', markersize=2)
    #ax.plot([x for x in range(1,35)], [y for y in pricesel[1][:9]], color='r', marker='s', markersize=2)
    plt.ylabel("Price out of 100")
    plt.grid(True)
    plt.xlabel("Query")
    lgd = plt.legend(['Average', 'Maximum', 'Minimum'], loc='lower left', ncol=2, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/benchmarkleakageinfogain', bbox_extra_artists=(lgd,), bbox_inches='tight')


def test():
    fig, ax = plt.subplots()
    ax.set_ylim([0, 15])
    ax.set_xlim([10, 400])
    ax.yaxis.set_ticks(np.arange(0, 15, 5))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks(np.arange(10, 400, 100))
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.2)
    ax.tick_params(
            axis='x',          # changes apply to the x-axis
            which='major',      # both major and minor ticks are affected
            bottom='on',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            direction='out',
            labelbottom='on') # labels along the bottom edge are off

    ax.tick_params(
            axis='y',
            which='major',
            left='on',
            right='off',
            direction='out')
    arr_x = [10, 20, 30, 40, 80, 160, 320]
    arr_y = [10.188, 8.34, 7.966, 4.33, 1.045, 1.067, 1.134]
    arr_y2 = [14.188, 14.34, 12.966, 10.566, 4.344, 1.067, 1.134]
    ax.plot(arr_x, arr_y, color='b', marker='x', markersize=2)
    ax.plot(arr_x, arr_y2, color='r', marker='x', markersize=2)
    plt.ylabel("Time in s")
    plt.grid(True)
    plt.legend(['Q1', 'Q2'], loc='upper right')
    plt.xlabel("Buffer pool size MB")
    plt.savefig('test.jpg', bbox_inches='tight')


if __name__ == '__main__':
    test()