import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

DATA =[[-2.67948021e-03, -4.28565398e-02, -8.20504375e-02,
        -1.30455112e-01, -1.60050003e-01, -2.00035179e-01],
       [ 2.25707813e-03, -4.01078618e-02, -8.36617255e-02,
        -1.37181931e-01, -1.60059679e-01, -1.99993722e-01],
       [-2.23113018e-03, -4.18923828e-02, -8.60432209e-02,
        -1.61098830e-01, -1.60167637e-01, -1.99609094e-01],
       [-2.42804816e-04, -4.06201468e-02, -8.93829334e-02,
        -1.19999487e-01, -1.55078447e-01, -1.96742534e-01],
       [ 5.42229476e-03, -3.68952625e-02, -9.01242325e-02,
        -1.24398238e-01, -1.54355808e-01, -1.95788471e-01],
       [ 2.54055420e-02, -1.80670875e-02, -7.25707083e-02,
        -1.34052637e-01, -1.31212561e-01, -1.85314341e-01],
       [ 5.65163628e-02,  1.39968209e-02, -4.09184981e-02,
        -1.07790721e-01, -1.03142536e-01, -1.63050681e-01],
       [ 8.31869572e-02,  4.45350558e-02,  6.65488995e-03,
        -4.77078070e-02, -7.39419514e-02, -1.28935648e-01],
       [ 1.12420501e-01,  7.45060830e-02,  3.03720266e-02,
        -1.24123911e-01, -5.16882274e-02, -1.01361518e-01],
       [ 1.40499992e-01,  1.01321272e-01,  6.96924756e-02,
         5.29300833e-02, -1.01962999e-02, -6.64721359e-02],
       [ 1.70765473e-01,  1.38540651e-01,  1.00906014e-01,
         6.54573207e-02,  9.48390178e-03, -2.94397021e-01],
       [ 2.04910944e-01,  1.66050935e-01,  1.40002957e-01,
         8.64295447e-02,  5.02643637e-02, -2.00000000e-01],
       [ 2.37365805e-01,  2.00243245e-01,  1.86501280e-01,
         8.11487234e-02,  8.25442907e-02, -2.00000000e-01],
       [ 2.83925006e-01,  2.49829652e-01,  2.09527212e-01,
         1.45508563e-01,  1.24579390e-01, -2.00000000e-01],
       [ 2.81844310e-01,  2.55334623e-01,  2.08262385e-01,
         2.33644176e-01,  1.28974413e-01, -2.00000000e-01],
       [ 2.80568862e-01,  2.57865561e-01,  2.09118826e-01,
         1.86431397e-01,  1.34997420e-01, -2.00000000e-01],
       [ 2.81562513e-01,  2.56431239e-01,  2.05138955e-01,
         2.17531254e-01,  1.71347403e-01, -2.00000000e-01],
       [ 2.82833546e-01,  2.53856076e-01,  1.94592164e-01,
         1.67129935e-01,  1.78926464e-01, -2.00000000e-01],
       [ 2.76346659e-01,  2.33005540e-01,  1.81594924e-01,
         1.12302523e-01,  1.12051295e-01, -2.00000000e-01],
       [ 2.48784592e-01,  1.85198133e-01,  1.42266546e-01,
         7.20308918e-02,  5.89843755e-02, -2.00000000e-01],
       [ 2.02377937e-01,  1.36032939e-01,  9.60065541e-02,
         8.22390835e-02,  6.24038891e-02, -2.00000000e-01]]
data =DATA[0:-1]
print(data)
ax = sns.heatmap(data, xticklabels=False, yticklabels=False)
plt.show()