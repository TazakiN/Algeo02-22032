import numpy as np

# Kiri masuk kanan engga
# di ujung kanan masuk
bins = [1, 26, 41, 121, 191, 271, 295, 316, 360] # your bins

hist, bin_edges = np.histogram(h,bins) # make the histogram

print(hist)