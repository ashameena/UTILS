import matplotlib.pyplot as plt
import numpy as np

Title = 'Required Time for\nInstrument Correction of 1000 waveforms'

x_label = 'Number of Processes'
y_label = 'Time (min)'
'''
# First line:
x = np.array([1,2,5,10,20,30,40,50,60,70])
y = np.array([433.3,218.62,95.47,54.97,33.82,27.17,26.35,26.5,23.82,25.99])

plt.plot(x,y,'o-', lw = 3, label = '1h waveforms')

# Second line:
x = np.array([1,2,5,10,20,30,40,50,60,70])
y = np.array([563.45,294.21,125.31,70.19,46.30,41.48,42.61,38.69,37.10,38.45])

plt.plot(x,y,'x-', lw = 3, label = '2h waveforms')

# Third line:
x = np.array([1,2,5,10,20,30,40,50,60,70])
y = np.array([982.73,506.38,229.97,138.96,125.3,144.48,130.5,129.32,133.78,131.78])

plt.plot(x,y,'v-', lw = 3, label = '5h waveforms')
'''

# First line:
x = np.array([1,2,5,10,20,30,40,50])
y = np.array([833.66,414.17,161.96,78.22,39.68,26.58,22.84,21.38])

plt.plot(x,y/60.,'o-', lw = 3, markersize = 8, c = '0.0', label = '1h waveforms')

# Second line:
x = np.array([1,2,5,10,20,30,40,50])
y = np.array([1010.61,504.09,195.95,96.85,50.91,36.36,30.59,29.49])

plt.plot(x,y/60., 'x-', lw = 3, markersize = 8, markeredgewidth = 2, c = '0.3', label = '2h waveforms')

# Third line:
x = np.array([1,2,5,10,20,30,40,50])
y = np.array([1382.86,679.12,273.97,147.01,86.75,75.60,73.25,73.96])

plt.plot(x,y/60.,'v-', lw = 3, markersize = 8, c = '0.5', label = '5h waveforms')





plt.title(Title, size = 'large', weight = 'bold')

plt.xticks([1,5,10,20,30,40,50], size = 'large', weight = 'bold')
plt.yticks(range(2,26,2),size = 'large', weight = 'bold')

plt.xlabel(x_label, size = 'large', weight = 'bold')
plt.ylabel(y_label, size = 'large', weight = 'bold')

plt.legend(loc=1)
plt.savefig('simple_line_plot.png')
plt.show()
