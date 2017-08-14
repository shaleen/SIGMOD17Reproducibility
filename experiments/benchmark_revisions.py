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
pricejoinnbrs = [[15.057528764382191, 15.057528764382191, 19.209604802401202, 24.712356178089045, 30.465232616308153, 38.06903451725863, 56.928464232116056, 70.63531765882941, 81.64082041020511, 87.99399699849926, 90.59529764882441, 91.59579789894947, 91.59579789894947, 94.14707353676839],
                 [75.08958096655844, 75.08958096655844, 78.29378354848477, 81.60798921174, 84.3615638425458, 87.29318614812256, 92.58756714421808, 95.42603271317394, 97.33118340254705, 98.31717343196082, 98.7004914704495, 98.84499812033094, 98.84499812033094, 99.20646287261265],
                 [33.01650825412706, 33.01650825412706, 40.07003501750876, 47.9239619809905, 54.97748874437219, 63.48174087043522, 78.68934467233616, 88.09404702351176, 92.79639819909956, 94.89744872436218, 95.847923961981, 96.29814907453726, 96.29814907453726, 97.49874937468735],
                 [55.11485107235959, 55.11485107235959, 64.0631971813821, 72.85603782381436, 79.70118125596063, 86.63145980193698, 95.41829443986626, 98.53746282846275, 99.43365880038569, 99.69126634352693, 99.77870375908314, 99.81388893546323, 99.81388893546323, 99.88771274081263]]
idealjoin = [5600/239,5600/239,6800/239,8300/239,9900/239,11900/239,15800/239,18700/239,20800/239,21800/239,22200/239,22400/239,22400/239,22800/239]
idealgroup = [0.26*500/25,0.26*1000/25,0.26*1500/25,0.26*2000/25,0.26*2500/25]

pricejoinrand = [[17.171717171717173, 17.171717171717173, 19.19191919191919, 22.22222222222222, 29.292929292929294, 37.37373737373738, 56.56565656565657, 72.72727272727273, 82.82828282828282, 88.88888888888889, 92.92929292929293, 93.93939393939394, 93.93939393939394, 95.95959595959596],
                 [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                 [61.657006486419114, 61.657006486419114, 64.0775230069396, 67.2679397745802, 73.27982598512305, 78.58158286205445, 87.6005810951209, 93.06974047457746, 95.89998500550932, 97.43677989915905, 98.40414884753437, 98.63941836077458, 98.63941836077458, 99.10246174465198],
                 [98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899, 98.98989898989899]]
pricejoinrandcov = [[12.057528764382191, 12.057528764382191, 16.209604802401202, 21.343434343434, 27.465232616308153, 33.06903451725863, 52.928464232116056, 65.63531765882941, 78.3243242342344, 84.23123123123, 86.34324234234, 88.4233223, 94.443442343242343, 98.4563222]]

pricegrpnbrs = [[7.808108108108109, 13.02002002002002, 17.027027027027028, 19.63163163163163, 20.93693693693694],
                [15.550285019754483, 31.01178756333911, 36.72099526954382, 38.22519716914111, 40.19272525779032],
                [11.192930458231984, 22.586821165481897, 30.24037483034576, 35.32787816663787, 41.078620813450364],
                [53.62538262191352, 66.71211062722512, 71.057198907731, 73.33497276289778, 75.57994070258701]]
pricegrprand = [[99.8998998998999, 99.8998998998999, 99.8998998998999, 99.8998998998999, 99.8998998998999],
                [100.0, 100.0, 100.0, 100.0, 100.0],[100.0, 100.0, 100.0, 100.0, 100.0],[100.0, 100.0, 100.0, 100.0, 100.0]]
pricegrprandcov = [[8.808108108108109, 10.02002002002002, 19.027027027027028, 19.63163163163163, 24.93693693693694]]
def benchjoin():
    mpl.rcParams['figure.figsize'] = 2.7, 1.95
    plt.yscale('log')
    fig, ax = plt.subplots()
    ax.set_xscale('log')
    ax.set_ylim([0, 105])
    #ax.set_xlim([-0.5, 100])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 105, 20))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    #ax.xaxis.set_ticks([1,16,32,64,100])
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

    a = [0,0.0750,0.1550,0.3125,0.625,1.25,2.5,5,10,20,40,60,80,100]

    ax.plot(a, [y for y in pricejoinnbrs[0]], color='b', marker='x', markersize=2)
    ax.plot(a, [y for y in pricejoinnbrs[1]], color='r', marker='s', markersize=2)
    ax.plot(a, [y for y in pricejoinnbrs[2]], color='g', marker='D', markersize=2)
    ax.plot(a, [y for y in pricejoinnbrs[3]], color='y', marker='^', markersize=2)
    ax.plot(a, [y for y in pricejoinrand[0]], color='khaki', marker='>', markersize=2)
    ax.plot(a, [y for y in pricejoinrand[1]], color='chocolate', marker='+', markersize=2)
    ax.plot(a, [y for y in pricejoinrand[2]], color='firebrick', marker='p', markersize=2)
    ax.plot(a, [y for y in pricejoinrand[3]], color='fuchsia', marker='<', markersize=2)
    #ax.plot(a, [y for y in pricejoinrandcov[0]], color='peru', marker='v', markersize=2)
    #ax.plot(a, idealjoin, color='m', marker='h', markersize=2)
    #plt.ylabel("Price")
    plt.grid(True)
    plt.xlabel("$u$ parameter in $Q^{\\bowtie}_u$")
    # lgd = plt.legend(['disagreementCount - nbrs', 'TsallisEntropy - nbrs',' Shannon Entropy - nbrs',  'Information Gain - nbrs',
    #                   'disagreementCount - uniform', 'TsallisEntropy - uniform',' Shannon Entropy - uniform',  'Information Gain - uniform'], loc='lower right', ncol=2, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/cameraready/experiments/benchmarkjoin', bbox_inches='tight')

def benchgrp():
    mpl.rcParams['figure.figsize'] = 2.5, 1.95
    fig, ax = plt.subplots()
    ax.set_ylim([0, 105])
    ax.set_xlim([4, 25])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 105, 20))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks([5,10,15,20,25])
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

    a = [5,10,15,20,25]

    ax.plot(a, [y for y in pricegrpnbrs[0]], color='b', marker='x', markersize=2)
    ax.plot(a, [y for y in pricegrpnbrs[1]], color='r', marker='s', markersize=2)
    ax.plot(a, [y for y in pricegrpnbrs[2]], color='g', marker='D', markersize=2)
    ax.plot(a, [y for y in pricegrpnbrs[3]], color='y', marker='^', markersize=2)
    ax.plot(a, [y for y in pricegrprand[0]], color='khaki', marker='>', markersize=2)
    ax.plot(a, [y for y in pricegrprand[1]], color='chocolate', marker='+', markersize=2)
    ax.plot(a, [y for y in pricegrprand[2]], color='firebrick', marker='p', markersize=2)
    ax.plot(a, [y for y in pricegrprand[3]], color='fuchsia', marker='<', markersize=2)
    #ax.plot(a, [y for y in pricegrprandcov[0]], color='peru', marker='v', markersize=2)
    #ax.plot(a, idealgroup, color='m', marker='h', markersize=2)
    #plt.ylabel("Price")
    plt.grid(True)
    plt.xlabel("$u$ parameter in $Q^{\gamma}_u$")

    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/cameraready/experiments/benchmarkgroup', bbox_inches='tight')


time_taken_sel = [0.0005345, 0.00345, 0.006455, 0.0156, 0.02237, 0.06677]
time_taken_proj = [0.0011, 0.00595, 0.01866, 0.0238, 0.0511, 0.11925]
time_taken_join = [0.004, 0.026, 0.044, 0.09245, 0.1819, 0.4473]
time_taken_agg = [0.0019, 0.0095, 0.02336, 0.06532, 0.0923, 0.144857]
support_size = [10, 50, 100, 200, 400, 1000]


def benchtime():
    mpl.rcParams['figure.figsize'] = 2.6, 1.95
    fig, ax = plt.subplots()
    ax.set_ylim([0, 0.45])
    ax.set_xlim([1, 1000])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0, 0.45, 0.1))
    #ax.yaxis.set_ticks(np.arange(0, 100, 2), minor=True)
    ax.xaxis.set_ticks([10, 200, 400, 1000])
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

    a = [10, 50, 100, 200, 400, 1000]

    ax.plot(a, time_taken_sel, color='b', marker='x', markersize=2)
    ax.plot(a, time_taken_proj, color='r', marker='s', markersize=2)
    ax.plot(a, time_taken_join, color='g', marker='D', markersize=2)
    ax.plot(a, time_taken_agg, color='y', marker='^', markersize=2)
    plt.ylabel("Time taken in s")
    plt.grid(True)
    plt.xlabel("Support Set size")
    lgd = plt.legend(['$Q^{\sigma}_{80}$','$Q^{\pi}_{4}$','$Q^{\\bowtie}_{80}$','$Q^{\gamma}_{20}$'], loc='upper left', ncol=2, bbox_to_anchor=(0, 1))
    plt.savefig('/Users/shaleen/Documents/UW-Madison/Paris/cs799_summer16.git/trunk/tobesubmitted/experiments/benchmarktimesssize', bbox_inches='tight',bbox_extra_artists=(lgd,))




if __name__ == '__main__':
    #benchtime()
    benchgrp()
    benchjoin()

