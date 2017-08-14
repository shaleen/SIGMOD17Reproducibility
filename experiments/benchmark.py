__author__ = 'shaleen'

from matplotlib import rc_file
rc_file('matplotlibrc-singlecolumn')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math
import matplotlib as mpl

mpl.rcParams['figure.figsize'] = 3.5, 1.95


#'disagreementCount', 'TsallisEntropy','bucketEntropy',  'disagreementEntropyCount'
pricesel = [[0.0, 0.7007007007007007, 1.901901901901902, 4.2042042042042045, 10.11011011011011, 20.42042042042042, 36.73673673673674, 65.76576576576576, 100.0, 100.0], [0.0, 1.395790184578971, 3.76572768965161, 8.227446665885108, 19.187555924292667, 36.6500634768903, 59.94022050078106, 88.21373926479032, 99.8998998998999, 99.8998998998999], [0.0, 0.8017959417645715, 2.1746349067326753, 4.7999343913617825, 11.457103273542979, 23.01200618483954, 40.87033560637888, 71.01872174226204, 100.0, 100.0], [0.0, 28.174015314267027, 42.63129463158064, 54.116147714378805, 66.82039054156634, 76.99882454614689, 85.50125257538207, 93.9324505705711, 100.0, 100.0]]
idealsel = [0, 100/239,300/239,700/239,1500/239,3100/239,6300/239,12700/239, 100]

priceproj = [[3.803803803803804, 15.915915915915916, 25.125125125125127, 33.033033033033036, 40.94094094094094, 48.848848848848846, 57.65765765765766, 64.86486486486487, 72.77277277277277, 79.87987987987988, 85.98598598598599, 92.3923923923924, 100.00], [7.459110762414067, 29.282335388441496, 43.91177964751538, 55.12058605151699, 65.07869230591953, 73.78609841072303, 82.01294387480573, 87.589691793896, 92.51333415497581, 95.87124662199737, 97.94940085230375, 99.32815698581464, 100.00], [4.343930704162791, 17.98616203880149, 28.20166047904138, 36.860516286187604, 45.38385241504743, 53.753419892170996, 62.86588768395974, 70.12550362864711, 77.84100403622602, 84.49062695437405, 89.91298330280753, 95.16953683918699, 100.00], [52.667081376214036, 73.39053382769823, 80.00071113300696, 83.9626255790601, 87.07005458820569, 89.62697539211618, 92.02741177875716, 93.7327428558137, 95.39829758980926, 96.74744234595946, 97.81393923046096, 98.85437449740782, 100.00]]
idealproj = [100/13, 200/13,300/13,400/13,500/13, 600/13, 700/13, 800/13, 900/13, 1000/13, 1100/13, 1200/13, 100]

priceprogrand = [[100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0], [99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592], [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0], [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]]

priceselrand = [[0.0, 82.91457286432161, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0], [0.0, 96.64907451832025, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592, 99.49748743718592], [0.0, 88.22299700124113, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0], [0.0, 96.46044660135998, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]]

priceseldprime = [[0.0, 0.4004004004004004, 1.8018018018018018, 4.504504504504505, 9.30930930930931, 20.12012012012012, 39.13913913913914, 67.06706706706707, 100.0], [0.0, 0.7987967947927888, 3.569335100866633, 8.801594387179968, 17.742667592517446, 36.17190764337912, 62.92017743469195, 89.08688468248029, 99.8996994992991], [0.0, 0.45825647590672647, 2.0603126408652694, 5.14177819686611, 10.59238421000831, 22.71825926719154, 43.49480439121538, 72.34302425558892, 99.97990833484558], [0.0, 20.071573489266793, 41.84847805559016, 55.115066507619225, 65.62560331757066, 76.78432314483844, 86.41840851852662, 94.21613943065591, 100.0]]

priceprojdprime = [[3.003003003003003, 12.412412412412412, 21.92192192192192, 30.03003003003003, 38.23823823823824, 46.446446446446444, 53.953953953953956, 60.56056056056056, 68.96896896896897, 77.07707707707708, 83.68368368368368, 91.69169169169169, 100.0], [5.912819726633545, 23.271720168617062, 39.016193370547725, 51.01197293389485, 61.81657132608084, 71.27367607848089, 78.7436084733382, 84.38468498528559, 90.30171312453594, 94.66824181538897, 97.25401076752428, 99.21793665537409, 99.8996994992991], [3.431200428309833, 14.093094803580964, 24.719367160206694, 33.647728863256, 42.547369535738525, 51.28859798125991, 59.124256427022104, 65.8734185141846, 74.22642634929898, 81.96594570620672, 87.96667289106719, 94.68446595956455, 99.97990833484558], [49.24450759677425, 69.79083115135909, 78.02610491509273, 82.5826695380701, 86.08124653543754, 88.89680825511584, 91.0661486108199, 92.73861116123418, 94.62101204485518, 96.23029523784874, 97.42098610313329, 98.74415095433001, 100.0]]


disagsel10 = [0.0, 0.0, 0.0, 0.0, 11.11111111111111, 22.22222222222222, 22.22222222222222, 66.66666666666667, 100.0]
shansel10 = [0.0, 0.0, 0.0, 0.0, 15.87603285713901, 31.118298643722476, 31.118298643722476, 83.33333333333333, 100.0]
disagsel20 = [0.0, 0.0, 5.2631578947368425, 5.2631578947368425, 5.2631578947368425, 5.2631578947368425, 26.31578947368421, 47.36842105263158, 100.0]
shansel20 = [0.0, 0.0, 7.002761887482012, 7.002761887482012, 7.002761887482012, 7.002761887482012, 33.95792636822195, 58.84150088949786, 100.0]
disagsel40 = [0.0, 0.0, 2.5641025641025643, 5.128205128205129, 10.256410256410257, 15.384615384615385, 30.76923076923077, 66.66666666666667, 100.0]
shansel40 = [0.0, 0.0, 3.2549452667794743, 6.491470160142199, 12.90723928091867, 19.242976998450402, 37.718170585812274, 76.66251583190667, 100.0]
disagsel80 = [0.0, 0.0, 2.5316455696202533, 2.5316455696202533, 2.5316455696202533, 8.860759493670885, 29.11392405063291, 59.49367088607595, 100.0]
shansel80 = [0.0, 0.0, 3.10364587717995, 3.10364587717995, 3.10364587717995, 10.796028434987448, 34.69623730347091, 67.87140072595523, 100.0]
disagsel160 = [0.0, 0.6289308176100629, 2.5157232704402515, 4.40251572327044, 9.433962264150944, 16.352201257861637, 38.36477987421384, 67.29559748427673, 100.0]
shansel160 = [0.0, 0.7526161080348981, 3.005732570913777, 5.251644154291457, 11.204417982021075, 19.298743212170088, 44.249196957864825, 74.50670601476169, 100.0]
disagsel160 = [0.0, 0.0, 2.5316455696202533, 2.5316455696202533, 2.5316455696202533, 8.860759493670885, 29.11392405063291, 59.49367088607595, 100.0]
shansel160 = [0.0, 0.7526161080348981, 3.005732570913777, 5.251644154291457, 11.204417982021075, 19.298743212170088, 44.249196957864825, 74.50670601476169, 100.0]
disagsel320 = [0.0, 0.39215686274509803, 1.5686274509803921, 3.1372549019607843, 7.8431372549019605, 16.07843137254902, 31.372549019607842, 61.1764705882353, 100.0]
shansel320 = [0.0, 0.4627882119691784, 1.8494766903914939, 3.694441935869208, 9.201526191311304, 18.733133566373727, 36.03514913862136, 67.80539867876226, 100.0]
disagsel512 = [0.0, 0.9784735812133072, 1.761252446183953, 4.109589041095891, 8.806262230919765, 19.17808219178082, 35.61643835616438, 64.77495107632095, 100.0]
shansel512 = [0.0, 1.1346014091423329, 2.0411669866135296, 4.75483051355261, 10.154257951106738, 21.89400103432133, 40.1186657449108, 70.58148375577181, 100]
disagsel512 = [0.0, 0.5865102639296188, 1.66177908113392, 5.083088954056696, 9.775171065493646, 17.693059628543498, 36.36363636363637, 64.71163245356794, 100.0]
shansel512 = [0.0, 0.6708890766596087, 1.8995535059995183, 5.797562283257928, 11.114328700215347, 20.005502823380795, 40.49424723836207, 69.976181766627, 99.98044690172244]
disagsel1024 = [0.0, 0.6600660066006601, 2.0502050205020503, 4.72047204720472, 9.990999099909992, 13.331933193319333, 26.14361436143614, 55.71657165716572, 99.9899989999]
shansel1024 = [0.0, 0.7173794713797865, 2.2365484703996907, 5.163597170228207, 10.906676104795455, 21.022392957841575, 38.96617952684161, 69.37536674646307, 99.8240476997121]


disagproj10 = [0.0, 0.0, 0.0, 22.22222222222222, 44.44444444444444, 55.55555555555556, 55.55555555555556, 66.66666666666667, 66.66666666666667, 66.66666666666667, 66.66666666666667, 88.88888888888889, 100.0]
disagproj160 = [1.0578616352201257, 8.578616352201259, 32.41509433962264, 32.704402515723274, 43.62264150943396, 40.685534591194966, 55.9748427672956, 66.66094339622641, 68.95597484276729, 85.50314465408805, 86.79245283018868, 93.08176100628931, 100.0]
disagproj1024 = [2.932551319648094, 13.782991202346041, 21.79863147605083, 29.52101661779081, 36.852394916911045, 43.79276637341153, 50.83088954056696, 59.33528836754643, 68.71945259042033, 77.90811339198436, 85.43499511241447, 93.05962854349951, 100.0]

onlycell1000dis = [17.81781781781782, 10.01001001001001]
onlycell1000shan = [19.843783264677807, 11.095363318612561]
onlyswap1000dis = [0.0, 0.0]
onlyswap1000shan = [0.0, 0.0]
half1000dis = [3.25, 3.70370]
quarter1000dis = [1.55, 1.87]
tquarter1000dis = [11.45, 7.895]
half1000shan = [4.26, 4.1897]

def ratio():
    mpl.rcParams['figure.figsize'] = 2.5, 1.95
    fig, ax = plt.subplots()
    ax.set_ylim([-1, 25])
    ax.set_xlim([0, 1])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 25, 5))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks([0, 0.25, 0.5, 0.75, 1])
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



    ax.plot([0, 0.25, 0.5, 0.75, 1], [onlycell1000dis[0], tquarter1000dis[0], half1000dis[0], quarter1000dis[0], onlyswap1000dis[0]], color='b', marker='x', markersize=2)
    ax.plot([0, 0.25, 0.5, 0.75, 1], [onlycell1000dis[1], tquarter1000dis[1], half1000dis[1], quarter1000dis[1], onlyswap1000dis[1]], color='m', marker='h', markersize=2)

    #plt.ylabel("Price")
    plt.grid(True)
    plt.xlabel("fraction of swap updates")
    lgd = plt.legend(['$Q^{r}_1$', '$Q^{r}_2$'], loc='upper left', ncol=4, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/tobesubmitted/experiments/benchmarkcellswapratio', bbox_extra_artists=(lgd,), bbox_inches='tight')

def benchselsize():
    mpl.rcParams['figure.figsize'] = 2.8, 1.95
    fig, ax = plt.subplots()
    ax.set_ylim([0, 105])
    ax.set_xlim([1, 239])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 105, 20))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks([1,32,64,128,239])
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

    a = [math.pow(2,x) for x in range(0,8)]
    a.append(239)

    ax.plot(a, disagsel10, color='b', marker='x', markersize=2)
    # ax.plot([math.pow(2,x) for x in range(0,9)], disagsel20, color='r', marker='s', markersize=2)
    # ax.plot([math.pow(2,x) for x in range(0,9)], disagsel40, color='g', marker='o', markersize=2)
    # ax.plot([math.pow(2,x) for x in range(0,9)], disagsel80, color='y', marker='^', markersize=2)
    ax.plot(a, disagsel160, color='r', marker='s', markersize=2)
    # ax.plot([math.pow(2,x) for x in range(0,9)], disagsel320, color='chocolate', marker='+', markersize=2)
    # ax.plot([math.pow(2,x) for x in range(0,9)], disagsel512, color='firebrick', marker='D', markersize=2)
    ax.plot(a, disagsel1024, color='g', marker='8', markersize=2)
    ax.plot(a, idealsel, color='m', marker='v', markersize=2)
    plt.ylabel("Price")
    plt.grid(True)
    plt.xlabel("$u$ parameter in $Q^{\sigma}_u$")
    lgd = plt.legend(['10','100','1000', 'Ideal price'], loc='lower right', ncol=1, bbox_to_anchor=(1, 0),prop={'size':6})
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/cameraready/experiments/benchmarkselectsupportsize', bbox_extra_artists=(lgd,), bbox_inches='tight')

def benchprojsize():
    mpl.rcParams['figure.figsize'] = 2.5, 1.95
    fig, ax = plt.subplots()
    ax.set_ylim([0, 105])
    ax.set_xlim([1, 13])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 105, 20))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks(np.arange(1, 14, 1))
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



    ax.plot([x for x in range(1,14)],disagproj10 , color='b', marker='x', markersize=2)
    ax.plot([x for x in range(1,14)], disagproj160, color='r', marker='s', markersize=2)
    ax.plot([x for x in range(1,14)],disagproj1024 , color='g', marker='8', markersize=2)
    ax.plot([x for x in range(1,14)], idealproj, color='m', marker='v', markersize=2)
    #plt.ylabel("Price")
    plt.grid(True)
    plt.xlabel("$u$ parameter in $Q^{\pi}_u$")
    lgd = plt.legend(['10','100','1000','Ideal price'], loc='lower right', ncol=1, bbox_to_anchor=(1, 0),prop={'size':6})
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/cameraready/experiments/benchmarkprojectsupportsize', bbox_extra_artists=(lgd,), bbox_inches='tight')

def benchsel():
    mpl.rcParams['figure.figsize'] = 2.5, 1.95
    fig, ax = plt.subplots()
    ax.set_ylim([0, 105])
    ax.set_xlim([1, 240])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 105, 20))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks([1,32,64,128,239])
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

    a = [math.pow(2,x) for x in range(0,8)]
    a.append(239)


    ax.plot(a, [y for y in pricesel[0][:9]], color='b', marker='x', markersize=2)
    ax.plot(a, [y for y in pricesel[1][:9]], color='r', marker='s', markersize=2)
    ax.plot(a, [y for y in pricesel[2][:9]], color='g', marker='D', markersize=2)
    ax.plot(a, [y for y in pricesel[3][:9]], color='y', marker='^', markersize=2)
    ax.plot(a, [y for y in priceselrand[0][:9]], color='khaki', marker='>', markersize=2)
    ax.plot(a, [y for y in priceselrand[1][:9]], color='chocolate', marker='+', markersize=2)
    ax.plot(a, [y for y in priceselrand[2][:9]], color='firebrick', marker='p', markersize=2)
    ax.plot(a, [y for y in priceselrand[3][:9]], color='fuchsia', marker='<', markersize=2)
    #ax.plot(a, [y for y in priceseldprime[0][:9]], color='peru', marker='v', markersize=2)
    #ax.plot(a, idealsel, color='m', marker='h', markersize=2)
    plt.ylabel("Price")
    plt.grid(True)
    plt.xlabel("$u$ parameter in $Q^{\sigma}_u$")
    #lgd = plt.legend(['disagreementCount - nbrs', 'TsallisEntropy - nbrs',' Shannon Entropy - nbrs',  'Information Gain - nbrs',
    #                  'disagreementCount - uniform', 'TsallisEntropy - uniform',' Shannon Entropy - uniform',  'Information Gain - uniform', 'Random coverage - nbrs', 'Ideal price'], loc='lower left', ncol=2, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/cameraready/experiments/benchmarkselect', bbox_inches='tight')

def benchproj():
    mpl.rcParams['figure.figsize'] = 2.5, 1.95
    fig, ax = plt.subplots()
    ax.set_ylim([0, 105])
    ax.set_xlim([1, 13])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 105, 20))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks(np.arange(1,14, 1))
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

    ax.plot([x for x in range(1,14)], [y for y in priceproj[0][:13]], color='b', marker='x', markersize=2)
    ax.plot([x for x in range(1,14)], [y for y in priceproj[1][:13]], color='r', marker='s', markersize=2)
    ax.plot([x for x in range(1,14)], [y for y in priceproj[2][:13]], color='g', marker='D', markersize=2)
    ax.plot([x for x in range(1,14)], [y for y in priceproj[3][:13]], color='y', marker='^', markersize=2)

    ax.plot([x for x in range(1,14)], [y for y in priceprogrand[0][:13]], color='khaki', marker='>', markersize=2)
    ax.plot([x for x in range(1,14)], [y for y in priceprogrand[1][:13]], color='chocolate', marker='+', markersize=2)
    ax.plot([x for x in range(1,14)], [y for y in priceprogrand[2][:13]], color='firebrick', marker='p', markersize=2)
    ax.plot([x for x in range(1,14)], [y for y in priceprogrand[3][:13]], color='fuchsia', marker='<', markersize=2)
    #ax.plot([x for x in range(1,14)], [y for y in priceprojdprime[0][:13]], color='peru', marker='v', markersize=2)
    #ax.plot([x for x in range(1,14)], idealproj, color='m', marker='h', markersize=2)
    #plt.ylabel("Price")
    handles,labels = ax.get_legend_handles_labels()
    plt.grid(True)
    plt.xlabel("$u$ parameter in $Q^{\pi}_u$")
    lgd = plt.legend(['coverage - nbrs', 'q-entropy - nbrs',' shannon entropy - nbrs',  'uniform info gain - nbrs',
                      'coverage - uniform', 'q-entropy - uniform',' shannon entropy - uniform',  'uniform info gain - uniform'], loc='lower left', ncol=4, bbox_to_anchor=(8.17, -0.05), fontsize = 'x-small')
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/cameraready/experiments/benchmarkproject',  bbox_inches='tight',bbox_extra_artists=(lgd,))

if __name__ == '__main__':
    #benchsel()
    #benchproj()
    benchselsize()
    #benchprojsize()
    # ratio()
    # benchproj()
    # benchprojrand()
    # benchselrand()
    # benchseldprime()
    # benchprojdprime()
