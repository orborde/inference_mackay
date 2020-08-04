'''Plot CDF for the log of the factor by which you'll update towards the truth after observing 1000 samples.
'''

import glob
import re
import numpy
import matplotlib.pyplot as plt

def cdf(a):
  counts, bin_edges = numpy.histogram(a, bins=100, density=True)
  cdf = numpy.cumsum(counts)
  cdf /= cdf[-1]
  return bin_edges, cdf

def main():
  for fn in glob.glob('outputs/I*-J*-N1000-T*.txt'):
    x, y = cdf([float(line) for line in open(fn)])
    label = re.sub(r'outputs/I(\d*)-J(\d*).*', lambda m: f'{m.group(1)} categories for Cause, {m.group(2)} categories for Effect', fn)
    plt.plot(x[1:], y, label=label)

  plt.legend()
  plt.xlim(-5, 5)
  plt.show()

if __name__ == "__main__":
    main()