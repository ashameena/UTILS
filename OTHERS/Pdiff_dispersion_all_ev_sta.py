import matplotlib.pyplot as plt
import numpy as np

x_label = 'Dominant Period (sec)'
#y_label = 'Time Difference (dT)'

x = np.array([2.7, 3.7, 5.3, 7.5, 10.6, 15.0, 21.2, 30.0])
y = np.array([-0.221, -0.234, -0.138, -0.036, -0.014, -0.04, -0.071, -0.156])

plt.plot(x,y,'o-', lw = 3, markersize = 8, c = '0.0', label = 'Mean dT (sec)')

x = np.array([2.7, 3.7, 5.3, 7.5, 10.6, 15.0, 21.2, 30.0])
y = np.array([86911, 61041, 42319, 43617, 54973, 70830, 90087, 123466])/100000.

plt.plot(x,y,'o-', lw = 3, color = 'r', markersize = 8, label = '#data/1e5.')

#x = np.array([2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015])
#y = np.array([2774912, 2475200, 3057252, 3742074, 5039724, 7068188, 7189264, 9521715, 11134284, 10867171, 10593555, 11844448, 10788348, 0, 0, 0])
plt.xticks(x, size = 'large', weight = 'bold', rotation=45)
#plt.yticks(range(2,26,2),size = 'large', weight = 'bold')
plt.yticks(size = 'large', weight = 'bold')

plt.xlabel(x_label, size = 'xx-large', weight = 'bold')
#plt.ylabel(y_label, size = 'xx-large', weight = 'bold')

plt.legend(loc=2)
#plt.savefig('simple_line_plot.png')
plt.show()

