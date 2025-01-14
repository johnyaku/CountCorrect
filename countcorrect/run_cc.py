### Function for running the CountCorrect algorithm.

# -*- coding: utf-8 -*-
r"""Run CountCorrect model to remove backgorund noise from Nanostring WTA data"""

import matplotlib.pyplot as plt
from countcorrect.ProbeCounts__GeneralModel import ProbeCounts_GeneralModel
import numpy as np

def run_countcorrect(counts_geneProbes, counts_negativeProbes, counts_nuclei,
                     n_factors = 30,
                     total_iterations = 20000,
                     learning_rate = 0.01,
                     posterior_samples = 100,
                     verbose = True,
                     naive = False):
    
    if not naive:
    
        if np.any(counts_nuclei == 0) or np.any(np.isnan(counts_nuclei)) or np.any(np.isinf(counts_nuclei)):
            raise ValueError('Some of your nuclei counts are 0, nan or inf')

        if verbose:

            print('Initializing model...')

        model = ProbeCounts_GeneralModel(
            X_data = counts_geneProbes,
            Y_data = counts_negativeProbes,
            nuclei = counts_nuclei,
            n_factors = n_factors)

        if verbose:

            print('Fitting model ...')

        model.fit_advi_iterative(n_iter = total_iterations, learning_rate = learning_rate, n=1, method='advi')

        if verbose:

            model.plot_history()
            plt.show()
            model.plot_history(iter_start = int(np.round(total_iterations - (total_iterations*0.1))),
                               iter_end = int(total_iterations))
            plt.show()

            print('Sampling from posterior distribution...')

        model.sample_posterior(node='all', n_samples=posterior_samples, save_samples=False);

        model.compute_X_corrected()          

        if verbose:

            print('Done.')
            
        return model.X_corrected_mean
            
    else:
        
        X_naive = np.round(np.clip(counts_geneProbes - np.mean(counts_negativeProbes, axis = 1).reshape(np.shape(counts_negativeProbes)[0],1), a_min = 0, a_max = None))
        
        return X_naive
              
