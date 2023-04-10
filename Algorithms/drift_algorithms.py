import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm
from sklearn.cluster import KMeans

######################################################################
# ATTACH
######################################################################

def attach(fixation_XY, line_Y):
	n = len(fixation_XY)
	for fixation_i in range(n):
		line_i = np.argmin(abs(line_Y - fixation_XY[fixation_i, 1]))
		fixation_XY[fixation_i, 1] = line_Y[line_i]
	return fixation_XY

# Implemnting fix_align function from the paper "Software for the automatic correction of recorded eye fixation locations in reading experiments"
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm
from sklearn.mixture import GaussianMixture

def fix_align(fixation_XY, line_Y):
    # Linear regression used to assign fixations to text lines:
    # Algorithm parameterized by slope, vertical offset, and standard deviation:

    # Fixation data:
    fixation_X = fixation_XY[:, 0]
    fixation_Y = fixation_XY[:, 1]

    # Assign fixations to text lines using Gaussian mixture model:
    n_components = len(line_Y)
    gmm = GaussianMixture(n_components=n_components, covariance_type='diag', max_iter=100)

    line_params = []
    fixation_Y_new = np.zeros_like(fixation_Y)

    # Find the minimum and maximum Y values
    min_y = np.min(line_Y)
    max_y = np.max(line_Y)

    for i, line_y in enumerate(line_Y):
        # Check if the current line is the last line
        if i == len(line_Y) - 1:
            next_line_y = max_y + 1  # set the next line y value as greater than the maximum y value
        else:
            next_line_y = line_Y[i+1]  # set the next line y value as the next line in the list

        # Text line data:
        line_X = np.mean(fixation_X[(fixation_Y >= line_y) & (fixation_Y < next_line_y)]) * np.ones_like(fixation_Y[(fixation_Y >= line_y) & (fixation_Y < next_line_y)])
        line_X = np.repeat(line_X, len(fixation_Y[(fixation_Y >= line_y) & (fixation_Y < next_line_y)]) // len(line_X))

        # Linear regression:
        def linear_regression(params):
            slope, offset, sigma = params
            line_Y_hat = slope * line_X + offset
            return np.sum(norm.pdf(fixation_Y[fixation_Y == line_y], line_Y_hat, sigma))

        # Optimize linear regression:
        params = minimize(linear_regression, [0, 0, 1], method='Nelder-Mead').x
        slope, offset, sigma = params
        line_params.append((slope, offset, sigma))

        # Assign fixations to text lines:
        line_Y_hat = slope * line_X + offset
        gmm.fit(line_Y_hat.reshape(-1, 1))
        line_weights = gmm.predict_proba(line_Y_hat.reshape(-1, 1))
        line_i = np.argmax(line_weights, axis=1)
        fixation_Y_new[fixation_Y == line_y] = np.take(line_Y, line_i)

    # Combine X and Y coordinates:
    fixation_XY[:, 1] = fixation_Y_new

    return fixation_XY





######################################################################
# CLUSTER
# 
# https://github.com/sascha2schroeder/popEye/
######################################################################

def cluster(fixation_XY, line_Y):
	m = len(line_Y)
	fixation_Y = fixation_XY[:, 1].reshape(-1, 1)
	clusters = KMeans(m, n_init=100, max_iter=300).fit_predict(fixation_Y)
	centers = [fixation_Y[clusters == i].mean() for i in range(m)]
	ordered_cluster_indices = np.argsort(centers)
	for fixation_i, cluster_i in enumerate(clusters):
		line_i = np.where(ordered_cluster_indices == cluster_i)[0][0]
		fixation_XY[fixation_i, 1] = line_Y[line_i]
	return fixation_XY

######################################################################
# COMPARE
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

def compare(fixation_XY, word_XY, x_thresh=512, n_nearest_lines=3):
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

#This function implements the same fixation detection and line break detection, however assigns fixation
# lines to text lines by comparing the fixation numbers rather than DTW

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
        line_scores = np.zeros(n_nearest_lines)
        for candidate_i in range(n_nearest_lines):
            candidate_line_i = nearest_line_I[candidate_i]
            text_line = word_XY[word_XY[:, 1] == line_Y[candidate_line_i]]
            Nf = len(gaze_line)
            Nw = len(text_line)
            if Nf == Nw:
                line_scores[candidate_i] = 0
            else:
                line_scores[candidate_i] = abs(Nf - Nw)
        line_i = nearest_line_I[np.argmin(line_scores)]
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

#This function implements the same fixation detection and line break detection, however assigns fixation
# lines to text lines by comparing the line length rather than DTW

def compare_line_len(fixation_XY, word_XY, x_thresh=512, n_nearest_lines=3):
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
        line_scores = np.zeros(n_nearest_lines)
        for candidate_i in range(n_nearest_lines):
            candidate_line_i = nearest_line_I[candidate_i]
            text_line = word_XY[word_XY[:, 1] == line_Y[candidate_line_i]]
            Lf = np.linalg.norm(gaze_line[-1, :] - gaze_line[0, :])
            Ll = np.linalg.norm(text_line[-1, :] - text_line[0, :])
            line_scores[candidate_i] = abs(Ll - Lf)
        line_i = nearest_line_I[np.argmin(line_scores)]
        fixation_XY[start_of_line:end_of_line, 1] = line_Y[line_i]
        start_of_line = end_of_line
    return fixation_XY


######################################################################
# MERGE
#
# Špakov, O., Istance, H., Hyrskykari, A., Siirtola, H., & Räihä,
#   K.-J. (2019). Improving the performance of eye trackers with
#   limited spatial accuracy and low sampling rates for reading
#   analysis by heuristic fixation-to-word mapping. Behavior Research
#   Methods, 51(6), 2661–2687.
#
# https://doi.org/10.3758/s13428-018-1120-x
# https://github.com/uta-gasp/sgwm
######################################################################

phases = [{'min_i':3, 'min_j':3, 'no_constraints':False}, # Phase 1
          {'min_i':1, 'min_j':3, 'no_constraints':False}, # Phase 2
          {'min_i':1, 'min_j':1, 'no_constraints':False}, # Phase 3
          {'min_i':1, 'min_j':1, 'no_constraints':True}]  # Phase 4

def merge(fixation_XY, line_Y, y_thresh=32, g_thresh=0.1, e_thresh=20):
	n = len(fixation_XY)
	m = len(line_Y)
	diff_X = np.diff(fixation_XY[:, 0])
	dist_Y = abs(np.diff(fixation_XY[:, 1]))
	sequence_boundaries = list(np.where(np.logical_or(diff_X < 0, dist_Y > y_thresh))[0] + 1)
	sequence_starts = [0] + sequence_boundaries
	sequence_ends = sequence_boundaries + [n]
	sequences = [list(range(start, end)) for start, end in zip(sequence_starts, sequence_ends)]
	for phase in phases:
		while len(sequences) > m:
			best_merger = None
			best_error = np.inf
			for i in range(len(sequences)-1):
				if len(sequences[i]) < phase['min_i']:
					continue # first sequence too short, skip to next i
				for j in range(i+1, len(sequences)):
					if len(sequences[j]) < phase['min_j']:
						continue # second sequence too short, skip to next j
					candidate_XY = fixation_XY[sequences[i] + sequences[j]]
					gradient, intercept = np.polyfit(candidate_XY[:, 0], candidate_XY[:, 1], 1)
					residuals = candidate_XY[:, 1] - (gradient * candidate_XY[:, 0] + intercept)
					error = np.sqrt(sum(residuals**2) / len(candidate_XY))
					if phase['no_constraints'] or (abs(gradient) < g_thresh and error < e_thresh):
						if error < best_error:
							best_merger = (i, j)
							best_error = error
			if best_merger is None:
				break # no possible mergers, break while and move to next phase
			merge_i, merge_j = best_merger
			merged_sequence = sequences[merge_i] + sequences[merge_j]
			sequences.append(merged_sequence)
			del sequences[merge_j], sequences[merge_i]
	mean_Y = [fixation_XY[sequence, 1].mean() for sequence in sequences]
	ordered_sequence_indices = np.argsort(mean_Y)
	for line_i, sequence_i in enumerate(ordered_sequence_indices):
		fixation_XY[sequences[sequence_i], 1] = line_Y[line_i]
	return fixation_XY

######################################################################
# REGRESS
#
# Cohen, A. L. (2013). Software for the automatic correction of
#   recorded eye fixation locations in reading experiments. Behavior
#   Research Methods, 45(3), 679–683.
#
# https://doi.org/10.3758/s13428-012-0280-3
# https://blogs.umass.edu/rdcl/resources/
######################################################################

def regress(fixation_XY, line_Y, k_bounds=(-0.1, 0.1), o_bounds=(-50, 50), s_bounds=(1, 20)):
	n = len(fixation_XY)
	m = len(line_Y)

	def fit_lines(params, return_line_assignments=False):
		k = k_bounds[0] + (k_bounds[1] - k_bounds[0]) * norm.cdf(params[0])
		o = o_bounds[0] + (o_bounds[1] - o_bounds[0]) * norm.cdf(params[1])
		s = s_bounds[0] + (s_bounds[1] - s_bounds[0]) * norm.cdf(params[2])
		predicted_Y_from_slope = fixation_XY[:, 0] * k
		line_Y_plus_offset = line_Y + o
		density = np.zeros((n, m))
		for line_i in range(m):
			fit_Y = predicted_Y_from_slope + line_Y_plus_offset[line_i]
			density[:, line_i] = norm.logpdf(fixation_XY[:, 1], fit_Y, s)
		if return_line_assignments:
			return density.argmax(axis=1)
		return -sum(density.max(axis=1))

	best_fit = minimize(fit_lines, [0, 0, 0])
	line_assignments = fit_lines(best_fit.x, True)
	for fixation_i, line_i in enumerate(line_assignments):
		fixation_XY[fixation_i, 1] = line_Y[line_i]
	return fixation_XY

######################################################################
# SEGMENT
#
# Abdulin, E. R., & Komogortsev, O. V. (2015). Person verification via
#   eye movement-driven text reading model, In 2015 IEEE 7th
#   International Conference on Biometrics Theory, Applications and
#   Systems. IEEE.
#
# https://doi.org/10.1109/BTAS.2015.7358786
######################################################################

def segment(fixation_XY, line_Y):
	n = len(fixation_XY)
	m = len(line_Y)
	diff_X = np.diff(fixation_XY[:, 0])
	saccades_ordered_by_length = np.argsort(diff_X)
	line_change_indices = saccades_ordered_by_length[:m-1]
	current_line_i = 0
	for fixation_i in range(n):
		fixation_XY[fixation_i, 1] = line_Y[current_line_i]
		if fixation_i in line_change_indices:
			current_line_i += 1
	return fixation_XY

######################################################################
# SPLIT
#
# Carr, J. W., Pescuma, V. N., Furlan, M., Ktori, M., & Crepaldi, D.
#   (2021). Algorithms for the automated correction of vertical drift
#   in eye-tracking data. Behavior Research Methods.
#
# https://doi.org/10.3758/s13428-021-01554-0
# https://github.com/jwcarr/drift
######################################################################

def split(fixation_XY, line_Y):
	n = len(fixation_XY)
	diff_X = np.diff(fixation_XY[:, 0])
	clusters = KMeans(2, n_init=10, max_iter=300).fit_predict(diff_X.reshape(-1, 1))
	centers = [diff_X[clusters == 0].mean(), diff_X[clusters == 1].mean()]
	sweep_marker = np.argmin(centers)
	end_line_indices = list(np.where(clusters == sweep_marker)[0] + 1)
	end_line_indices.append(n)
	start_of_line = 0
	for end_of_line in end_line_indices:
		mean_y = np.mean(fixation_XY[start_of_line:end_of_line, 1])
		line_i = np.argmin(abs(line_Y - mean_y))
		fixation_XY[start_of_line:end_of_line, 1] = line_Y[line_i]
		start_of_line = end_of_line
	return fixation_XY

######################################################################
# STRETCH
#
# Lohmeier, S. (2015). Experimental evaluation and modelling of the
#   comprehension of indirect anaphors in a programming language
#   (Master’s thesis). Technische Universität Berlin.
#
# http://www.monochromata.de/master_thesis/ma1.3.pdf
######################################################################

def stretch(fixation_XY, line_Y, scale_bounds=(0.9, 1.1), offset_bounds=(-50, 50)):
	n = len(fixation_XY)
	fixation_Y = fixation_XY[:, 1]

	def fit_lines(params, return_correction=False):
		candidate_Y = fixation_Y * params[0] + params[1]
		corrected_Y = np.zeros(n)
		for fixation_i in range(n):
			line_i = np.argmin(abs(line_Y - candidate_Y[fixation_i]))
			corrected_Y[fixation_i] = line_Y[line_i]
		if return_correction:
			return corrected_Y
		return sum(abs(candidate_Y - corrected_Y))

	best_fit = minimize(fit_lines, [1, 0], bounds=[scale_bounds, offset_bounds])
	fixation_XY[:, 1] = fit_lines(best_fit.x, return_correction=True)
	return fixation_XY

######################################################################
# WARP
#
# Carr, J. W., Pescuma, V. N., Furlan, M., Ktori, M., & Crepaldi, D.
#   (2021). Algorithms for the automated correction of vertical drift
#   in eye-tracking data. Behavior Research Methods.
#
# https://doi.org/10.3758/s13428-021-01554-0
# https://github.com/jwcarr/drift
######################################################################

def warp(fixation_XY, word_XY):
	# Call the dynamic time warping (dtw) function to find the best path between the two sequences
    # dtw_path stores the mapping between fixations and words

	_, dtw_path = dynamic_time_warping(fixation_XY, word_XY)

	# For each fixation, find the corresponding words and calculate the mode of their Y values
	for fixation_i, words_mapped_to_fixation_i in enumerate(dtw_path):
		# The Y values of the corresponding words
		candidate_Y = word_XY[words_mapped_to_fixation_i, 1]
		# The mode of the Y values of the corresponding words
        # is assigned as the Y value of the current fixation
		fixation_XY[fixation_i, 1] = mode(candidate_Y)

	# Return the corrected fixation data
	return fixation_XY

# Extension - Creating a version of the warp function that detects regressions and adapts to them
def warp_with_regression(fixation_XY, word_XY, words_sorted, aoi_lines, correct_data):
		
	# Filtering the fixation data to remove the regressions
	fixation_XY, correct_data = filter_out_regressions(fixation_XY, words_sorted, aoi_lines, correct_data)

	fixation_XY = np.array(fixation_XY.copy(), dtype=int)
	durations = np.delete(fixation_XY, 0, 1)
	durations = np.delete(durations, 0, 1)
	fixation_XY = np.delete(fixation_XY, 2, 1)


	_, dtw_path = dynamic_time_warping(fixation_XY, word_XY)

	# For each fixation, find the corresponding words and calculate the mode of their Y values
	for fixation_i, words_mapped_to_fixation_i in enumerate(dtw_path):
		# The Y values of the corresponding words
		candidate_Y = word_XY[words_mapped_to_fixation_i, 1]
		# The mode of the Y values of the corresponding words
        # is assigned as the Y value of the current fixation
		fixation_XY[fixation_i, 1] = mode(candidate_Y)

	# Return the corrected fixation data
	return fixation_XY, correct_data

# The mode function is used to find the most frequent value in a list
def mode(values):
	# Convert the input values to a list
	values = list(values)
	# Return the most frequent value in the list
	return max(set(values), key=values.count)


def time_warp(fixation_XY, word_XY):
    # Remove the durations from the fixation data
    durations = np.delete(fixation_XY, 0, 1)
    durations = np.delete(durations, 0, 1)
    fixation_XY = np.delete(fixation_XY, 2, 1)

    # Remove the durations from the word data
    word_durations = np.delete(word_XY, 0, 1)
    word_durations = np.delete(word_durations, 0, 1)
    word_XY = np.delete(word_XY, 2, 1)
    
	# Call the dynamic time warping (dtw) function to find the best path between the two sequences
    # dtw_path stores the mapping between fixations and words
    _, dtw_path = dynamic_time_warping(durations, word_durations)

    # For each fixation, find the corresponding words and calculate the mode of their Y values
    for fixation_i, words_mapped_to_fixation_i in enumerate(dtw_path):
		# The Y values of the corresponding words
        candidate_Y = word_XY[words_mapped_to_fixation_i, 1]
		# The mode of the Y values of the corresponding words
        # is assigned as the Y value of the current fixation
        fixation_XY[fixation_i, 1] = mode(candidate_Y)

	# Return the corrected fixation data
    return fixation_XY


######################################################################
# Dynamic Time Warping adapted from https://github.com/talcs/simpledtw
# This is used by the COMPARE and WARP algorithms
######################################################################

def dynamic_time_warping(sequence1, sequence2):
	n1 = len(sequence1)
	n2 = len(sequence2)
	dtw_cost = np.zeros((n1+1, n2+1))
	dtw_cost[0, :] = np.inf
	dtw_cost[:, 0] = np.inf
	dtw_cost[0, 0] = 0
	for i in range(n1):
		for j in range(n2):
			this_cost = np.sqrt(sum((sequence1[i] - sequence2[j])**2))
			dtw_cost[i+1, j+1] = this_cost + min(dtw_cost[i, j+1], dtw_cost[i+1, j], dtw_cost[i, j])
	dtw_cost = dtw_cost[1:, 1:]
	dtw_path = [[] for _ in range(n1)]
	while i > 0 or j > 0:
		dtw_path[i].append(j)
		possible_moves = [np.inf, np.inf, np.inf]
		if i > 0 and j > 0:
			possible_moves[0] = dtw_cost[i-1, j-1]
		if i > 0:
			possible_moves[1] = dtw_cost[i-1, j]
		if j > 0:
			possible_moves[2] = dtw_cost[i, j-1]
		best_move = np.argmin(possible_moves)
		if best_move == 0:
			i -= 1
			j -= 1
		elif best_move == 1:
			i -= 1
		else:
			j -= 1
	dtw_path[0].append(0)
	return dtw_cost[-1, -1], dtw_path

def filter_out_regressions(fixations, words_sorted, aoi_lines, correct_data):
	'''Filters out regression fixations from the list of fixations'''

	new_fixations = [] # creates an empty list `new_fixations` to store the non-regression fixations

	new_corrected_data = [] # creates an empty list `new_corrected_data` to store the non-regression fixations

	# Variable to store the current line number
	line_number = 0
    
	for i, fix in enumerate(fixations): # loop through the list of fixations
		x, y, duration = fix[0], fix[1], fix[2] # unpack the values from each fixation

		# Use the aoi_lines to determine when to increment the line number
		if y > aoi_lines.at[line_number, 'y'] + aoi_lines.at[line_number, 'height']:
			line_number += 1

		is_regression = False # initialize the `is_regression` flag as False

		# check if this fixation is a regression within line
		words_on_line = words_sorted[line_number]
		recent_words = [word for word in words_on_line if word[0] < x]
		if len(recent_words) > 0:
			last_word_x, last_word_y = recent_words[-1][0], recent_words[-1][1]
			if x < last_word_x:
				is_regression = True

		# check if this fixation is a regression between lines
		if not is_regression and line_number > 0:
			for j in range(i-1, -1, -1):
				prev_x, prev_y = fixations[j][0], fixations[j][1]
				if prev_y <= y and y <= aoi_lines.at[line_number, 'y']:
					# we found a fixation on the previous line, so this must be a regression
					is_regression = True
					break

		if not is_regression: # if this fixation is not a regression, add it to the new list of fixations
			new_fixations.append([x, y, duration])
			new_corrected_data.append(correct_data[i])

	return new_fixations, new_corrected_data # return the final list of non-regression fixations
