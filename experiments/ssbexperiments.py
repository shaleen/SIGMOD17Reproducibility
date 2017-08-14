__author__ = 'shaleen'

from matplotlib import rc_file
rc_file('matplotlibrc-singlecolumn')
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import numpy as np
mpl.rcParams['figure.figsize'] = 3.4, 1.95
mpl.rcParams['xtick.labelsize'] = 5
mpl.rcParams['legend.fontsize'] = 7
#ordering 'disagreementCount', 'bucketEntropy', 'TsallisEntropy', 'disagreementEntropyCount' size 250
dis = [0.4500900180036007, 0.0, 0.0, 1.220244048809762, 1.0602120424084818, 0.8301660332066413, 3.030606121224245, 0.2500500100020004, 0.12002400480096019, 0.010002000400080016, 1.9703940788157632, 2.6105221044208844, 0.590118023604721]
dishistorydata = [0.4500900180036007, 0.4500900180036007, 0.4500900180036007, 1.6255881063180319, 2.5100432204532442, 3.1413178011854886, 4.8264926949230871, 5.0691504886492531, 5.1536507899951252, 5.1536507899951252, 5.9982092072754449, 6.9114478566128632, 6.9475987577356078]
diff = [0,0,0,0.05, 0.22, 0.42, 1.53, 1.81, 1.81, 1.84, 2.94, 4.63, 5.19 ]
timediff = [0,0,0,0.05, 0.17, 0.20, 1.11, 0.28, 0, 0, 0.03, 1.10, 2, 1.69, 0.56]
weighteddis = [0.5134368432101314, 0.0, 0.0, 1.348674586516591, 0.9441568266697709, 0.9825815941454722, 2.5685182713969215, 0.2427063349931646, 0.08587286470774516, 0.0013556599209155276, 2.0767935914960836, 2.54638302754685, 0.7412309190732246]
weighteddishistory = [0.51333415584148934, 0.51333415584148934, 0.51333415584148934, 1.8255881063180319, 2.6100432204532442, 3.2413178011854886, 4.8264926949230871, 5.0691504886492531, 5.1536507899951252, 5.1536507899951252, 5.9982092072754449, 6.9114478566128632, 6.9475987577356078]
historytime =        [0.918865203857, 0.911951065063, 0.9123456, 0.865936279297, 0.848054885864, 0.837087631226, 0.818967819, 0.808000564575, 0.784158706665, 0.784158706665, 0.77486038208, 0.760078430176, 0.75056383]

historytime =        [0.1018, 0.0912, 0.645, 2.5877, 2.6993, 2.98, 3.3735, 3.7356, 3.9241, 3.8772, 3.5626, 3.8263, 4.2418]
historytimecumulative = [0.1018, 0.192, 0.838, 3.4257, 6.125, 9.105, 12.48, 16.21, 20.13, 24.01, 27.57, 31.40, 35.6417]
historytimecumulativesavings = [0.1018, 0.192, 0.838, 3.38, 5.96, 8.8786, 10.95, 14.68, 18.6 , 22.40, 24.57, 27.3, 31.85]



ssbcumprice = [0.032, 0.078, 1.467, 1.854, 2.467, 2.532, 2.78, 3.42, 3.97, 4.23, 4.47, 4.97, 4.99, 5.36, 5.734, 6.18, 6.34, 6.98, 7.323,
                                7.55, 8.345, 8.78, 9.767, 10.12, 10.19]
ssbcumpricesavings = [0.032, 0.078, 1.067, 1.098, 1.098, 1.25, 1.78,1.78, 1.97, 1.99, 1.99, 2.67, 2.93, 2.93, 2.93, 3.38, 3.78, 3.92, 3.92,
                                4.56, 4.56, 4.84, 4.84, 4.84, 4.84]



def disagreement():
    fig, ax = plt.subplots()
    ax.set_ylim([-0.5, 10.0])
    ax.set_xlim([0, 14])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0.0, 10.0, 2.0))
    ax.yaxis.set_ticks(np.arange(0.0, 10.0, 0.50), minor=True)
    ax.xaxis.set_ticks(np.arange(1,14, 1))
    ax.set_xticklabels(['$Q1.1$','$Q1.2$','$Q1.3$','$Q2.1$','$Q2.2$','$Q2.3$','$Q3.1$','$Q3.2$','$Q3.3$','$Q3.4$','$Q4.1$','$Q4.2$','$Q4.3$'])
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    #plt.gca().xaxis.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.2)
    ax.tick_params(
            axis='x',          # changes apply to the x-axis
            #which='major',      # both major and minor ticks are affected
            bottom='on',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            direction='out',
            labelbottom='on') # labels along the bottom edge are off

    ax.tick_params(
            axis='y',
            #which='major',
            left='on',
            right='off',
            direction='out')



    ax.plot([x for x in range(1,14)], dis, color='r', marker='o', linestyle = 'None')
    ax.plot([x for x in range(1,14)], weighteddis, color='g', marker='>',  linestyle = 'None')

    #ax.set_title('Static Analysis with support set 100000')
    plt.ylabel("Price out of 100")
    plt.xlabel("Query")
    lgd = plt.legend(['uniform weights', 'non-uniform weights'], loc='lower left', ncol=2, bbox_to_anchor=(0, 1.05))
    plt.savefig('ssbstatic100000', bbox_extra_artists=(lgd,), bbox_inches='tight')


def disagreementhistory():
    fig, ax = plt.subplots()
    ax.set_ylim([-0.5, 10.0])
    ax.set_xlim([0, 14])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0.0, 10.0, 2.0))
    ax.yaxis.set_ticks(np.arange(0.0, 10.0, 0.50), minor=True)
    ax.xaxis.set_ticks(np.arange(1,14, 1))
    ax.set_xticklabels(['$Q1.1$','$Q1.2$','$Q1.3$','$Q2.1$','$Q2.2$','$Q2.3$','$Q3.1$','$Q3.2$','$Q3.3$','$Q3.4$','$Q4.1$','$Q4.2$','$Q4.3$'])
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



    ax.plot([x for x in range(1,14)], weighteddishistory, color='g', marker='<', markersize=2, linestyle = 'None')

    ax.set_title('Static Analysis with support set 100000')
    plt.ylabel("Price out of 100")
    plt.xlabel("Query")
    lgd = plt.legend(['non-uniform weights'], loc='upper center', ncol=2, bbox_to_anchor=(0.85, 1.2))
    plt.savefig('ssbstatichistory100000', bbox_extra_artists=(lgd,), bbox_inches='tight')

def dishistorytime():
    fig, ax = plt.subplots()
    ax.set_ylim([0, 40])
    ax.set_xlim([0, 14])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 40, 10))
    #ax.yaxis.set_ticks(np.arange(0, 40, 1), minor=False)
    ax.xaxis.set_ticks(np.arange(1,14, 1))
    ax.set_xticklabels(['$Q1.1$','$Q1.2$','$Q1.3$','$Q2.1$','$Q2.2$','$Q2.3$','$Q3.1$','$Q3.2$','$Q3.3$','$Q3.4$','$Q4.1$','$Q4.2$','$Q4.3$'])
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



    ax.plot([x for x in range(1,14)], historytimecumulative, color='b', marker='x', markersize=2)
    ax.plot([x for x in range(1,14)], historytimecumulativesavings, color='r', marker='s', markersize=2)

    #ax.set_title('Static Analysis with support set 100000')
    plt.ylabel("Time in s")
    plt.xlabel("Query")
    lgd = plt.legend(['history-oblivious', 'history-aware'], loc='upper left', ncol=1, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/tobesubmitted/experiments/ssbstatichistorytime100000', bbox_extra_artists=(lgd,), bbox_inches='tight')

def dishistory():
    fig, ax = plt.subplots()
    ax.set_ylim([0, 15])
    ax.set_xlim([0, 14])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 15, 5))
    #ax.yaxis.set_ticks(np.arange(0, 15, 1), minor=False)
    ax.xaxis.set_ticks(np.arange(1,14, 1))
    ax.set_xticklabels(['$Q1.1$','$Q1.2$','$Q1.3$','$Q2.1$','$Q2.2$','$Q2.3$','$Q3.1$','$Q3.2$','$Q3.3$','$Q3.4$','$Q4.1$','$Q4.2$','$Q4.3$'])
    #ax.grid(which='minor', alpha=0.2)
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



    ax.plot([x for x in range(1,14)], [sum(dis[:i]) for i in range(1, 14)], color='b', marker='x', markersize=2)
    ax.plot([x for x in range(1,14)], dishistorydata, color='r', marker='s', markersize=2)
    plt.ylabel("Price")
    plt.xlabel("Query")
    lgd = plt.legend(['history-oblivious', 'history-aware'], loc='upper left', ncol=1, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/tobesubmitted/experiments/ssbstatichistoryawareprice', bbox_extra_artists=(lgd,), bbox_inches='tight')

def disbar():
    plt.yscale('log')
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.set_ylim([0.05,1000])
    ax.set_xlim([0.8, 14])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    #ax.yaxis.set_ticks((1,10,100))
    width = 0.2
    #ax.yaxis.set_ticks(np.arange(0, 15, 1), minor=False


    ax.xaxis.set_ticks([x + width for x in range(1,14)])
    ax.set_xticklabels(['$Q1.1$','$Q1.2$','$Q1.3$','$Q2.1$','$Q2.2$','$Q2.3$','$Q3.1$','$Q3.2$','$Q3.3$','$Q3.4$','$Q4.1$','$Q4.2$','$Q4.3$'])
    #ax.grid(which='minor', alpha=0.2)
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


    no_sampling = [0.12,	0.094,	0.065,	4.50,	4.78,	5.26,	5.87	,6.59,	7.42,	7.82,	6.45,	7.72,	8.03]
    naive = [1.23,	1.12,	0.89,	144,	168,	278,	393,  434,  	474,	525,	736,	672,	694]
    with_sampling = [0.10,	0.091,	0.064,	2.58,	2.69,	2.98,	3.37,	3.73,	3.92	,3.87	,3.56	,3.82,	4.24]
    qt = [2.39,	1.11	,1.22,	6.35,	5.72,	5.27,	5.56	,2.49 ,3.62,	3.67,	4.78,	4.68,	4.065]



    ax.bar([x - 0.5*width for x in range(1,14)], naive, width, color='blueviolet', linewidth=0.5, bottom = 0)
    ax.bar([x + 0.5*width for x in range(1,14)], with_sampling, width, color='dodgerblue', linewidth=0.5, bottom = 0)
    ax.bar([x + 1.5*width for x in range(1,14)], qt, width, color='darkorange', linewidth=0.5, bottom = 0)
    plt.ylabel("Time in s")
    plt.xlabel("Query")
    lgd = plt.legend(['no batching','with batching', 'query execution time'], loc='upper left', ncol=1, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/barchartssbtime', bbox_extra_artists=(lgd,), bbox_inches='tight')
    #4.44, 1.95

def disbartpch():
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.set_ylim([0.05,10000])
    ax.set_xlim([0, 7])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    #ax.yaxis.set_ticks((1,20,5))
    width = 0.2
    #ax.yaxis.set_ticks(np.arange(0, 15, 1), minor=False


    ax.xaxis.set_ticks([x + width for x in range(1,10)])
    ax.set_xticklabels(['$Q1$','$Q2$','$Q4$','$Q5$','$Q6$','$Q11$','$Q12$','$Q17$'])
    #ax.grid(which='minor', alpha=0.2)
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


    no_sampling = [0.12,	0.094,	0.065,	4.50,	4.78,	5.26,	5.87	,6.59,	7.42,	7.82,	6.45,	7.72,	8.03]
    naive = [1600,	530,	493,	2140,	593,	278,	727,  113]
    with_sampling = [0.66,	6.77,	1.58,	9.86,	0.52,	4.45,	14.89,	0.85]
    qt = [10.39,	3.51	,1.656,	14.156,	1.540,	0.589,	5.27	,0.5]



    ax.bar([x - 0.5*width for x in range(1,9)], naive, width, color='blueviolet',  linewidth=0.5, bottom = 0)
    ax.bar([x + 0.5*width for x in range(1,9)], with_sampling, width, color='dodgerblue', linewidth=0.5, hatch='////////////////')
    ax.bar([x + 1.5*width for x in range(1,9)], qt, width, color='darkorange', linewidth=0.5, hatch='\\\\\\\\\\\\\\\\\\')
    plt.ylabel("Time in s")
    plt.xlabel("Query")
    lgd = plt.legend(['no batching','with batching', 'query execution time'], loc='upper right', ncol=3, bbox_to_anchor=(1, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/experiments/barcharttpchtimetest', bbox_extra_artists=(lgd,), bbox_inches='tight')


def dishistoryq1():
    fig, ax = plt.subplots()
    mpl.rcParams['figure.figsize'] = 2.1, 1.95
    ax.set_ylim([0, 11])
    ax.set_xlim([0, 25])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 11, 5))
    #ax.yaxis.set_ticks(np.arange(0, 40, 1), minor=False)
    ax.xaxis.set_ticks(np.arange(0,26, 5))
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



    ax.plot([x for x in range(1,26)], ssbcumprice, color='b', marker='>', markersize=2)
    ax.plot([x for x in range(1,26)], ssbcumpricesavings, color='r', marker='s', markersize=2)
    plt.ylabel("Price")
    plt.xlabel("Query 1.1")
    lgd = plt.legend(['history-oblivious', 'history-aware'], loc='upper left', ncol=1, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/cameraready/experiments/ssbq11', bbox_extra_artists=(lgd,), bbox_inches='tight')

if __name__ == '__main__':
    #dishistorytime()
    #dishistory()
    # disbar()
    # disbartpch()
    #test()
    dishistoryq1()
