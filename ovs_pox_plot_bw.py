from matplotlib import pyplot
import matplotlib.patches as mpatches

pyplot.xlabel('Number of hosts')
pyplot.ylabel('BW Gbits/sec from 1st to last host')
pyplot.title("BW analysis while scaling hosts in a virtual DCN")

list_bw_pox = []
x_axis = [2**(i+2) for i in range(len(list_rtt_pox))]
pyplot.plot(x_axis, list_rtt_pox, 'ro-')


list_bw_ovs = [22.3, 21.4, 13.7, 11.2, 12.6, 10.7, 5.18, 3.54, 2.8]
x_axis = [2**(i+2) for i in range(len(list_rtt_ovs))]
pyplot.plot(x_axis, list_rtt_ovs, 'bo-')

red_patch = mpatches.Patch(color='red', label='POX')
blue_patch = mpatches.Patch(color='blue', label='OVS')
pyplot.legend(handles=[red_patch, blue_patch])


pyplot.savefig("ovs_vs_pox_rtt")
pyplot.close()


