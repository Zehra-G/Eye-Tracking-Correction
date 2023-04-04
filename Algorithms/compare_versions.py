import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

######################################################################
# COMPARE BY FIXATION NUMBER
#
# Lima Sanches, C., Kise, K., & Augereau, O. (2015). Eye gaze and text
#   line matching for reading analysis. In Adjunct proceedings of the
#   2015 ACM International Joint Conference on Pervasive and
#   Ubiquitous Computing and proceedings of the 2015 ACM International
#   Symposium on Wearable Computers (pp. 1227–1233). Association for
#   Computing Machinery.
#
# https://doi.org/10.1145/2800835.2807936
######################################################################

def compare_fixnum(fixation_XY, word_XY, x_thresh=512, n_nearest_lines=3):
	line_Y = np.unique(word_XY[:, 1])
	n = len(fixation_XY)
	diff_X = np.diff(fixation_XY[:, 0])
	end_line_indices = list(np.where(diff_X < -x_thresh)[0] + 1)
	end_line_indices.append(n)
	start_of_line = 0
	for end_of_line in end_line_indices:
		gaze_line = fixation_XY[start_of_line:end_of_line]
		mean_y = np.mean(gaze_line[:, 1])
		lines_ordered_by_proximity = np.argsort(abs(line_Y - mean_y))
		nearest_line_I = lines_ordered_by_proximity[:n_nearest_lines]
		line_costs = np.zeros(n_nearest_lines)
		for candidate_i in range(n_nearest_lines):
			candidate_line_i = nearest_line_I[candidate_i]
			text_line = word_XY[word_XY[:, 1] == line_Y[candidate_line_i]]
			dtw_cost, _ = dynamic_time_warping(gaze_line[:, 0:1], text_line[:, 0:1])
			line_costs[candidate_i] = dtw_cost
		line_i = nearest_line_I[np.argmin(line_costs)]
		fixation_XY[start_of_line:end_of_line, 1] = line_Y[line_i]
		start_of_line = end_of_line
	return fixation_XY

######################################################################
# COMPARE BY LINE LENGTH
#
# Lima Sanches, C., Kise, K., & Augereau, O. (2015). Eye gaze and text
#   line matching for reading analysis. In Adjunct proceedings of the
#   2015 ACM International Joint Conference on Pervasive and
#   Ubiquitous Computing and proceedings of the 2015 ACM International
#   Symposium on Wearable Computers (pp. 1227–1233). Association for
#   Computing Machinery.
#
# https://doi.org/10.1145/2800835.2807936
######################################################################

def compare_line_len(fixation_XY, word_XY, x_thresh=512, n_nearest_lines=3):
	return 
