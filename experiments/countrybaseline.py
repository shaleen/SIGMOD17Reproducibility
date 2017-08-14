__author__ = 'shaleen'

from matplotlib import rc_file
rc_file('matplotlibrc-singlecolumn')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

#ordering 'disagreementCount', 'bucketEntropy', 'TsallisEntropy', 'disagreementEntropyCount' size 250
neighbors_of_random = [[0.8032128514056225, 0.0, 0.40160642570281124, 0.0, 0.0, 0.40160642570281124, 1.2048192771084338, 0.40160642570281124, 2.0080321285140563, 33.734939759036145, 0.40160642570281124, 10.040160642570282, 1.606425702811245, 0.0, 0.0, 0.40160642570281124, 0.0, 1.606425702811245, 0.0, 0.0, 0.0, 32.1285140562249, 0.0, 0.0, 17.269076305220885, 6.024096385542169, 0.40160642570281124, 0.0, 0.0, 2.4096385542168677, 0.0, 6.827309236947791, 4.016064257028113, 68.27309236947791], [0.8472972698490899, 0.0, 0.47424844238607156, 0.0, 0.0, 0.47424844238607156, 1.421863631971465, 0.47424844238607156, 2.267389145099985, 38.67717753750235, 0.47424844238607156, 11.765298477476149, 1.8952279929600468, 0.0, 0.0, 0.47424844238607156, 0.0, 1.8952279929600468, 0.0, 0.0, 0.0, 36.89590920731144, 0.0, 0.0, 20.111666552189046, 7.082354676509695, 0.47424844238607156, 0.0, 0.0, 2.8410642086342808, 0.0, 8.021475430629266, 4.72913216819083, 74.87444460098057], [1.5935226851179873, 0.0, 0.799987096982302, 0.0, 0.0, 0.799987096982302, 2.39028402767697, 0.799987096982302, 3.964452186255063, 55.95393622683504, 0.799987096982302, 19.03195109756294, 3.180593861389336, 0.0, 0.0, 0.799987096982302, 0.0, 3.180593861389336, 0.0, 0.0, 0.0, 53.805583780906765, 0.0, 0.0, 31.48658892598506, 11.661102240286446, 0.799987096982302, 0.0, 0.0, 4.751536265544109, 0.0, 13.161078047128271, 7.854712020773857, 89.65984419606136], [12.562811021079627, 0.0, 0.0, 0.0, 0.0, 0.0, 19.911584372057668, 0.0, 29.169943860605375, 80.30547576912433, 0.0, 58.33988772121075, 25.125622042159254, 0.0, 0.0, 0.0, 0.0, 25.125622042159254, 0.0, 0.0, 0.0, 79.42118794492387, 0.0, 0.0, 68.16913866366745, 49.08152823266305, 0.0, 0.0, 0.0, 32.47439539313729, 0.0, 51.35002323031321, 41.732754881685004, 93.08277811199822]]
neighbors_of_d = [[0.8032128514056225, 0.0, 1.606425702811245, 0.0, 0.0, 0.40160642570281124, 2.0080321285140563, 2.8112449799196786, 0.8032128514056225, 34.53815261044177, 0.40160642570281124, 6.827309236947791, 4.016064257028113, 0.8032128514056225, 2.0080321285140563, 0.0, 0.0, 0.8032128514056225, 0.0, 0.40160642570281124, 0.0, 20.883534136546185, 0.0, 0.0, 18.87550200803213, 4.819277108433735, 0.0, 0.0, 0.0, 1.2048192771084338, 0.0, 7.6305220883534135, 3.6144578313253013, 69.07630522088354], [0.9482033824682046, 0.0, 1.8952279929600468, 0.0, 0.0, 0.47424844238607156, 2.3682952577190997, 3.313533618069686, 0.9482033824682046, 39.565175354845586, 0.47424844238607156, 8.021475430629266, 4.72913216819083, 0.9482033824682046, 2.3682952577190997, 0.0, 0.0, 0.9482033824682046, 0.0, 0.47424844238607156, 0.0, 24.242505500645795, 0.0, 0.0, 21.9512046157064, 5.671343858453026, 0.0, 0.0, 0.0, 1.421863631971465, 0.0, 8.959341197236348, 4.257568851102123, 75.65425286524079], [1.5967484395412956, 0.0, 3.180593861389336, 0.0, 0.0, 0.799987096982302, 3.9676779406783713, 5.532168835986518, 1.5967484395412956, 57.0087579232593, 0.799987096982302, 13.161078047128271, 7.854712020773857, 1.5967484395412956, 3.9676779406783713, 0.0, 0.0, 1.5967484395412956, 0.0, 0.799987096982302, 0.0, 37.321978677763255, 0.0, 0.0, 34.112353026564094, 9.386945371848842, 0.0, 0.0, 0.0, 2.39028402767697, 0.0, 14.64815083627683, 7.083756713601397, 90.15983613167529], [12.562811021079627, 0.0, 25.125622042159254, 0.0, 0.0, 0.0, 29.169943860605375, 35.2682693549074, 12.562811021079627, 80.73194968474708, 0.0, 51.35002323031321, 41.732754881685004, 12.562811021079627, 29.169943860605375, 0.0, 0.0, 12.562811021079627, 0.0, 0.0, 0.0, 71.61354691606296, 0.0, 0.0, 69.78125004342186, 45.03720641421692, 0.0, 0.0, 0.0, 19.911584372057668, 0.0, 53.365910582636445, 39.823168744115335, 93.2947607058267]]
random_subset = [[6.626506024096386, 0.0, 96.3855421686747, 0.8032128514056225, 2.4096385542168677, 32.53012048192771, 98.79518072289157, 98.39357429718875, 94.37751004016064, 100.0, 34.53815261044177, 100.0, 100.0, 88.75502008032129, 88.35341365461848, 68.67469879518072, 3.21285140562249, 93.57429718875503, 21.285140562248998, 63.45381526104418, 0.0, 100.0, 0.0, 0.0, 100.0, 100.0, 24.899598393574298, 2.4096385542168677, 21.285140562248998, 82.73092369477912, 4.417670682730924, 100.0, 99.59839357429719, 100.0], [26.742941465714242, 0.0, 98.56060835864643, 0.8472972698490899, 2.0585486569924205, 17.66999212592846, 99.76010139310773, 99.25557083001218, 93.6894625708574, 100.0, 35.055475435077746, 100.0, 100.0, 92.90600070182995, 92.45038949562961, 74.03555043607616, 3.7857022482435942, 96.56919217095015, 20.384627259574305, 70.02032410898005, 0.0, 100.0, 0.0, 0.0, 100.0, 100.0, 28.797152355512367, 2.0585486569924205, 24.598758516349093, 86.15825776118015, 5.200390930524257, 100.0, 100.0, 100.0], [71.75690714665892, 0.0, 99.48226641505782, 1.5935226851179873, 4.703149949194363, 50.21854486217965, 99.58871631102724, 99.56613603006403, 99.16614248157288, 99.59839357429718, 56.81521265786036, 99.59839357429718, 99.59839357429718, 98.3693811390139, 98.27260850631441, 89.85661521588362, 6.309575652005616, 99.20485153465268, 37.73487524394768, 86.38570345639587, 0.0, 99.59839357429718, 0.0, 0.0, 99.59839357429718, 99.59839357429718, 43.49929839841293, 4.703149949194363, 37.95100079030983, 96.60489346946018, 8.622441573523009, 99.59839357429718, 99.59839357429718, 99.59839357429718], [89.69283441547951, 0.0, 99.33277231698155, 12.562811021079627, 32.47439539313729, 79.64633748823067, 99.7803087627606, 99.70648257042019, 98.95119390402722, 100.0, 80.73194968474708, 100.0, 100.0, 97.8379481042169, 97.75575156805262, 93.1890793267518, 37.688433063238875, 98.79628436988448, 71.95878221445399, 91.7560172787485, 0.0, 100.0, 0.0, 0.0, 100.0, 100.0, 74.8014430297999, 32.47439539313729, 71.95878221445399, 96.56405353643169, 43.46018566528797, 100.0, 99.92706507195915, 100.0]]
ring = [[42.94975688816856, 0.0, 81.19935170178282, 0.0, 0.0, 0.0, 95.13776337115073, 84.76499189627229, 85.73743922204214, 99.3517017828201, 0.0, 95.78606158833063, 94.81361426256078, 87.03403565640194, 84.92706645056727, 79.90275526742302, 0.0, 86.54781199351702, 0.0, 73.257698541329, 0.0, 98.05510534846029, 0.0, 0.0, 99.18962722852513, 84.44084278768233, 0.0, 0.0, 0.0, 78.44408427876823, 0.0, 94.81361426256078, 92.86871961102106, 99.67585089141005], [15.111036059612859, 0.0, 34.83042504970778, 0.0, 0.0, 0.0, 32.021976488769965, 29.50033454055444, 32.629717326720794, 80.24689498853841, 0.0, 46.96863239170741, 44.55440483273973, 28.08906089002885, 27.256581561877347, 7.809459902297244, 0.0, 45.68595428607559, 0.0, 9.037987073705544, 0.0, 73.91819129514788, 0.0, 0.0, 66.75666491256797, 49.24194241727926, 0.0, 0.0, 0.0, 17.670718439098685, 0.0, 50.84796550705407, 40.921680636864174, 92.72795913426553], [57.802563247165004, 0.0, 87.30853794041855, 0.0, 0.0, 0.0, 79.98339852215327, 82.18151824717815, 86.66969626125262, 99.27683752354284, 0.0, 93.11327619132678, 92.7034928773881, 82.54454423426996, 79.33877784753433, 32.1165045483321, 0.0, 92.98613829136119, 0.0, 39.18158917121325, 0.0, 98.9479601459459, 0.0, 0.0, 98.23294079944522, 94.12985402782849, 0.0, 0.0, 0.0, 61.77903748203914, 0.0, 95.16324348746615, 91.56398004670478, 99.70868609284744], [86.84581436952867, 0.0, 96.75848765094466, 0.0, 0.0, 0.0, 99.22419890752894, 97.42737853136819, 97.60492250543106, 99.89876699517178, 0.0, 99.32990063549778, 99.17107762858085, 97.83854069429557, 97.45711019202945, 96.50794671412118, 0.0, 97.75134427787332, 0.0, 95.15652625889639, 0.0, 99.69430402703202, 0.0, 0.0, 99.87335552891759, 97.36774428361466, 0.0, 0.0, 0.0, 96.22118184377898, 0.0, 99.17107762858085, 98.84848536343115, 99.9494658009869]]

x_plot_rearranged = [5,4,3,2,1,6,11,8,7,9,10,       15,17,16,14,19,18,13,12       ,27,20,28,21,24,23,26,25,22      ,31,29,30,33,32,34]


def disagreement():
    linestyles = [(0, (2.0, 1.5)), '-']
    fig, ax = plt.subplots()
    ax.set_ylim([-5, 105.0])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0.0, 105.0, 10.0))
    ax.yaxis.set_ticks(np.arange(0.0, 100.0, 5.0), minor=True)
    ax.xaxis.set_ticks([1,11,19,28,34])
    ax.xaxis.set_ticks(np.arange(1, 34, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle=':', linewidth=1, dashes=[2,1,2], alpha=1)
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

    splits = [(1,12), (13,20), (21,29), (29,34)]
    for i in range(0, len(splits)):
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_random[0][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='r', marker='o', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_d[0][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='g', marker='v', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [random_subset[0][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='b', marker='s', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [ring[0][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='m', marker='+', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])

    ax.set_title('Disagreement')
    plt.ylabel("Price out of 100")
    plt.xlabel("Query index")
    lgd = plt.legend(['neighbors of D\'', 'Neighbors of D', 'Random', 'Ring'], loc='upper center', ncol=2, bbox_to_anchor=(0.85, 1.2))
    plt.savefig('disagreement', bbox_extra_artists=(lgd,), bbox_inches='tight')

def bucket():
    linestyles = [(0, (2.0, 1.5)), '-']
    fig, ax = plt.subplots()
    ax.set_ylim([-5, 105.0])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0.0, 105.0, 10.0))
    ax.yaxis.set_ticks(np.arange(0.0, 100.0, 5.0), minor=True)
    ax.xaxis.set_ticks([1,11,19,28,34])
    ax.xaxis.set_ticks(np.arange(1, 34, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle=':', linewidth=1, dashes=[2,1,2], alpha=1)
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

    splits = [(1,12), (13,20), (21,29), (29,34)]
    for i in range(0, len(splits)):
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_random[1][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='r', marker='o', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_d[1][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='g', marker='v', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [random_subset[1][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='b', marker='s', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [ring[1][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='m', marker='+', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
    ax.set_title('Bucket Entropy')
    plt.ylabel("Price out of 100")
    plt.xlabel("Query index")
    lgd = plt.legend(['neighbors of D\'', 'Neighbors of D', 'Random', 'Ring'], loc='upper center', ncol=2, bbox_to_anchor=(0.85, 1.2))
    plt.savefig('bucket', bbox_extra_artists=(lgd,), bbox_inches='tight')

def tsallis():
    linestyles = [(0, (2.0, 1.5)), '-']
    fig, ax = plt.subplots()
    ax.set_ylim([-5, 105.0])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0.0, 105.0, 10.0))
    ax.yaxis.set_ticks(np.arange(0.0, 100.0, 5.0), minor=True)
    ax.xaxis.set_ticks([1,11,19,28,34])
    ax.xaxis.set_ticks(np.arange(1, 34, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle=':', linewidth=1, dashes=[2,1,2], alpha=1)
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

    splits = [(1,12), (13,20), (21,29), (29,34)]
    for i in range(0, len(splits)):
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_random[2][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='r', marker='o', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_d[2][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='g', marker='v', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [random_subset[2][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='b', marker='s', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [ring[2][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='m', marker='+', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
    ax.set_title('Tsallis Entropy')
    plt.ylabel("Price out of 100")
    plt.xlabel("Query index")
    lgd = plt.legend(['neighbors of D\'', 'Neighbors of D', 'Random', 'Ring'], loc='upper center', ncol=2, bbox_to_anchor=(0.85, 1.2))
    plt.savefig('tsallis', bbox_extra_artists=(lgd,), bbox_inches='tight')

def aps():
    linestyles = [(0, (2.0, 1.5)), '-']
    fig, ax = plt.subplots()
    ax.set_ylim([-5, 105.0])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0.0, 105.0, 10.0))
    ax.yaxis.set_ticks(np.arange(0.0, 100.0, 5.0), minor=True)
    ax.xaxis.set_ticks([1,11,19,28,34])
    ax.xaxis.set_ticks(np.arange(1, 34, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle=':', linewidth=1, dashes=[2,1,2], alpha=1)
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

    splits = [(1,12), (13,20), (21,29), (29,34)]
    for i in range(0, len(splits)):
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_random[3][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='r', marker='o', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_d[3][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='g', marker='v', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [random_subset[3][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='b', marker='s', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [ring[3][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='m', marker='+', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
    ax.set_title('APS Entropy')
    plt.ylabel("Price out of 100")
    plt.xlabel("Query index")
    lgd = plt.legend(['neighbors of D\'', 'Neighbors of D', 'Random', 'Ring'], loc='upper center', ncol=2, bbox_to_anchor=(0.85, 1.2))
    plt.savefig('aps', bbox_extra_artists=(lgd,), bbox_inches='tight')


def neighbors_dprime():
    linestyles = [(0, (2.0, 1.5)), '-']
    fig, ax = plt.subplots()
    ax.set_ylim([-5, 105.0])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0.0, 105.0, 10.0))
    ax.yaxis.set_ticks(np.arange(0.0, 100.0, 5.0), minor=True)
    ax.xaxis.set_ticks([1,11,19,28,34])
    ax.xaxis.set_ticks(np.arange(1, 34, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle=':', linewidth=1, dashes=[2,1,2],alpha=1)
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

    splits = [(1,12), (13,20), (21,29), (29,34)]
    for i in range(0, len(splits)):
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_random[0][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='r', marker='o', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_random[1][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='g', marker='v', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_random[2][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='b', marker='s', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_random[3][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='m', marker='+', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
    ax.set_title('Neighbors of random D')
    plt.ylabel("Price out of 100")
    plt.xlabel("Query index")
    lgd = plt.legend(['Disagreement', 'Bucket', 'Tsallis', 'APS'], loc='upper center', ncol=2, bbox_to_anchor=(0.85, 1.2))
    plt.savefig('neighborsdprime', bbox_extra_artists=(lgd,), bbox_inches='tight')


def neighbors_d():
    linestyles = [(0, (2.0, 1.5)), '-']
    fig, ax = plt.subplots()
    ax.set_ylim([-5, 105.0])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0.0, 105.0, 10.0))
    ax.yaxis.set_ticks(np.arange(0.0, 100.0, 5.0), minor=True)
    ax.xaxis.set_ticks([1,11,19,28,34])
    ax.xaxis.set_ticks(np.arange(1, 34, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle=':', linewidth=1, dashes=[2,1,2], alpha=1)
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

    splits = [(1,12), (13,20), (21,29), (29,34)]
    for i in range(0, len(splits)):
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_d[0][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='r', marker='o', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_d[1][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='g', marker='v', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_d[2][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='b', marker='s', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [neighbors_of_d[3][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='m', marker='+', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
    ax.set_title('Neighbors of D')
    plt.ylabel("Price out of 100")
    plt.xlabel("Query index")
    lgd = plt.legend(['Disagreement', 'Bucket', 'Tsallis', 'APS'], loc='upper center', ncol=2, bbox_to_anchor=(0.85, 1.2))
    plt.savefig('neighborsd', bbox_extra_artists=(lgd,), bbox_inches='tight')

def random():
    linestyles = [(0, (2.0, 1.5)), '-']
    fig, ax = plt.subplots()
    ax.set_ylim([-5, 105.0])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0.0, 105.0, 10.0))
    ax.yaxis.set_ticks(np.arange(0.0, 100.0, 5.0), minor=True)
    ax.xaxis.set_ticks([1,11,19,28,34])
    ax.xaxis.set_ticks(np.arange(1, 34, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle=':', linewidth=1, dashes=[2,1,2], alpha=1)
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

    splits = [(1,12), (13,20), (21,29), (29,34)]
    for i in range(0, len(splits)):
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [random_subset[0][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='r', marker='o', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [random_subset[1][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='g', marker='v', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [random_subset[2][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='b', marker='s', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [random_subset[3][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='m', marker='+', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
    ax.set_title('Random')
    plt.ylabel("Price out of 100")
    plt.xlabel("Query index")
    lgd = plt.legend(['Disagreement', 'Bucket', 'Tsallis', 'APS'], loc='upper center', ncol=2, bbox_to_anchor=(0.85, 1.2))
    plt.savefig('random', bbox_extra_artists=(lgd,), bbox_inches='tight')

def ring_s():
    linestyles = [(0, (2.0, 1.5)), '-']
    fig, ax = plt.subplots()
    ax.set_ylim([-5, 105.0])
    ax.set_xlim([1, 34])
    #plt.gca().yaxis.grid(which='major', linestyle='--', linewidth=0.3)
    ax.yaxis.set_ticks(np.arange(0.0, 105.0, 10.0))
    ax.yaxis.set_ticks(np.arange(0.0, 100.0, 5.0), minor=True)
    ax.xaxis.set_ticks([1,11,19,28,34])
    ax.xaxis.set_ticks(np.arange(1, 34, 1), minor=True)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    plt.gca().xaxis.grid(which='major', linestyle=':', linewidth=1, dashes=[2,1,2], alpha=1)
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

    splits = [(1,12), (13,20), (21,29), (29,34)]
    for i in range(0, len(splits)):
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [ring[0][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='r', marker='o', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [ring[1][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='g', marker='v', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [ring[2][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='b', marker='s', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
        ax.plot([x for x in range(splits[i][0], splits[i][1])], [ring[3][x_plot_rearranged[x-1] - 1] for x in range(splits[i][0], splits[i][1])], color='m', marker='+', markersize=2, linestyle=':', linewidth=0.8, dashes=[1,2])
    ax.set_title('Ring')
    plt.ylabel("Price out of 100")
    plt.xlabel("Query index")
    lgd = plt.legend(['Disagreement', 'Bucket', 'Tsallis', 'APS'], loc='upper center', ncol=2, bbox_to_anchor=(0.85, 1.2))
    plt.savefig('ring', bbox_extra_artists=(lgd,), bbox_inches='tight')


if __name__ == '__main__':
    disagreement()
    bucket()
    tsallis()
    aps()
    neighbors_dprime()
    neighbors_d()
    random()
    ring_s()
