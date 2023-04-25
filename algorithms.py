from drift_algorithms_osf import * 
from Algorithms.ModeOfDisparities import correction_mode_of_disparities
from Algorithms.optimal_gaze_offset import *
from Algorithms.hill_climbing.src.make_cluster import *
from Algorithms.hill_climbing.src.correct_clusters import *


def hill_climbing(fixations, aois):
    
    clusters = make_cluster_refactor(fixations)
    corrections = correct_cluster(clusters, aois)
    
    if len(clusters) == 0:
        return fixations
    
    list_fix = []
    for c in corrections:
        x = c.autoxCorrected
        y = c.autoyCorrected
        list_fix.append[x, y]
        
        
    
    return list_fix

