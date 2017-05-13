from matplotlib import pyplot
import matplotlib.patches as mpatches

pyplot.xlabel('Number of hosts')
pyplot.ylabel('Avg RTT from 1st to last host')
pyplot.title("RTT analysis while scaling hosts in a virtual DCN")

#list_rtt_first = [4.985, 12.365, 19.918, 56.778, 101.403, 219.558, 582.469 ]
#list_rtt_second = [2.521, 6.843, 7.205, 26.552, 42.500, 77.770, 213.736]
list_rtt_first = [16.1, 21.5, 23.8, 49.6, 102, 117, 145]
list_rtt_second = [13.8, 14.8, 16.7, 19.7, 45.4, 93, 120]

red_patch = mpatches.Patch(color='red', label='h(1) -> h(n)')
blue_patch = mpatches.Patch(color='blue', label='h(n) -> h(1)')
pyplot.legend(handles=[red_patch, blue_patch])

x_axis = [2**(i+2) for i in range(len(list_rtt_first))]

pyplot.plot(x_axis, list_rtt_first, 'ro-')
pyplot.plot(x_axis, list_rtt_second, 'bo-')

pyplot.savefig("fatrttplot")
pyplot.close()


