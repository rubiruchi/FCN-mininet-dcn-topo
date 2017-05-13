from matplotlib import pyplot

pyplot.xlabel('Number of hosts')
pyplot.ylabel('Available Bandwidth Gbits/sec')
pyplot.title("Performance analysis for Fat Tree topology")
"""
list_band_plain = [22.3, 21.4, 13.7, 11.2, 12.6, 10.7, 5.18, 3.54, 2.8]
x_axis = [2**(i+2) for i in range(len(list_band_plain))]
pyplot.plot(x_axis, list_band_plain, 'ro-')
"""
list_band_fat = [21, 18.6, 18.4, 16.2, 8.67, 11.2, 7.67]
x_axis = [2**(i+2) for i in range(len(list_band_fat))]
pyplot.plot(x_axis, list_band_fat, 'bo-')

pyplot.savefig("fat_tree")
pyplot.close()


