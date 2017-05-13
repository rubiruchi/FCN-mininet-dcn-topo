from matplotlib import pyplot

pyplot.xlabel('Number of hosts')
pyplot.ylabel('Available Bandwidth Gbits/sec')
pyplot.title("Performance analysis while scaling hosts in a virtual DCN")
list_band = [22.3, 21.4, 13.7, 11.2, 12.6, 10.7, 5.18, 3.54, 2.8]
x_axis = [2**(i+2) for i in range(len(list_band))]

pyplot.plot(x_axis, list_band, marker='o')

pyplot.savefig("finplot")
pyplot.close()


