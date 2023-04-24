import numpy as np

def get_centers_of_aoi(aois):
    result = []

    for _, aoi in aois.iterrows():
        if aoi["kind"] == "sub-line":
            result.append((aoi["x"] + aoi["width"] / 2, aoi["y"] + aoi["height"]))

    return result

def dist(x1, x2, y1, y2):
    return np.sqrt((((x1-x2)**2) + ((y1-y2)**2)))

def compute_disparity_of_fixation(fixation, centers):
    closest = None
    closest_distance = float("inf")


    for center in centers:
        distance = dist(fixation[0], center[0], fixation[1], center[1])
        if distance < closest_distance:
            closest_distance = distance
            closest = center

    return closest[0] - fixation[0], closest[1] - fixation[1]

def get_disparities(aois, fixations):
    centers = get_centers_of_aoi(aois)
    disparities = []
    for fixation in fixations:
        disparity_x, disparity_y = compute_disparity_of_fixation(fixation, centers)
        disparities.append((disparity_x, disparity_y))

    return disparities

def gaussian(x):
    return np.exp(- (x ** 2))

def mean_shift(disparities, start_x, start_y, h):
    def sub_iteration(x, y, h_sub):
        # compute weights =  gaussian (current center - points) ** 2
        weights = []
        weight_sum = 0
        for disparity in disparities:
            d = dist(disparity[0], x, disparity[1], y) 
            d_over_h = d / h
            gauss = gaussian(d_over_h)
            weight = gauss ** 2
            #print(f"d{d}, d/h{d_over_h}, wght{weight}")
            weights.append(weight)
            weight_sum += weight

        # compute weighted sum over x and y
        result_x, result_y = 0, 0
        for weight, disparity in zip(weights, disparities):
            #print(f"w{weight}, disp{disparity}")
            result_x += weight / weight_sum * disparity[0]
            result_y += weight / weight_sum * disparity[1]

        return result_x, result_y
    
    TOLERANCE = h / 100

    x, y = start_x, start_y
    last_x, last_y = start_x, start_y
    #print("starting sub iteration seed")
    new_x, new_y = sub_iteration(last_x, last_y, h)
    sub_iterations = 1
    while dist(new_x, last_x, new_y, last_y) >= TOLERANCE:
        #print(f"starting sub iteration no {sub_iterations}. dist: {dist(new_x, last_x, new_y, last_y) }")
        sub_iterations += 1
        temp_x, temp_y = new_x, new_y
        h_sub = h / sub_iterations
        new_x, new_y =  sub_iteration(new_x, new_y, h_sub)
        last_x, last_y = temp_x, temp_y
    
    return new_x, new_y

def correction_mode_of_disparities(fixations, aois):
    #print("starting get_disparities")
    disparities = get_disparities(aois, fixations)
    #print("got disparities")
 
    H_ESTIMATE = dist(max(aois["width"]),  min(aois["width"]), max(aois["height"]), min(aois["height"])) #(max(aois["width"]) -  min(aois["width"]) ** 2 + max(aois["height"]) -  min(aois["height"]) ** 2) ** 0.5
    iterations = 1
    TOLERANCE = H_ESTIMATE / 100
    
    #print("mean_shift no 0")
    last_x, last_y = mean_shift(disparities, 0, 0, H_ESTIMATE)
    #print("mean shift no 1")
    new_x, new_y =  mean_shift(disparities, last_x, last_y, H_ESTIMATE)
    #print("starting loop!")
    while dist(new_x, last_x, new_y, last_y) >= TOLERANCE:
        #print(f"iteration {iterations}, {dist(new_x, last_x, new_y, last_y)}")
        iterations += 1
        temp_x, temp_y = new_x, new_y
        new_x, new_y =  mean_shift(disparities, new_x, new_y, H_ESTIMATE / iterations)
        last_x, last_y = temp_x, temp_y

    new_fixations = []
    for fixation in fixations:
        fixation[0] -= new_x
        fixation[1] -= new_y
        new_fixations.append(fixation)
        
    return new_fixations