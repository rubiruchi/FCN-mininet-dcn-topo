from matplotlib import pyplot
import matplotlib.patches as mpatches

pyplot.xlabel('Number of hosts')
pyplot.ylabel('Avg RTT from 1st to last host')
pyplot.title("RTT analysis while scaling hosts in a virtual DCN")

list_rtt_pox = [91.307, 122.649, 202,687, 237.452, 497.402, 1101 ]
x_axis = [2**(i+2) for i in range(len(list_rtt_pox))]
pyplot.plot(x_axis, list_rtt_pox, 'ro-')


list_rtt_ovs = [4.985, 12.365, 19.918, 56.778, 101.403, 219.558, 582.469 ]
x_axis = [2**(i+2) for i in range(len(list_rtt_ovs))]
pyplot.plot(x_axis, list_rtt_ovs, 'bo-')

red_patch = mpatches.Patch(color='red', label='POX')
blue_patch = mpatches.Patch(color='blue', label='OVS')
pyplot.legend(handles=[red_patch, blue_patch])


pyplot.savefig("ovs_vs_pox_rtt")
pyplot.close()


