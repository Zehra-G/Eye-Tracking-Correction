def get_centers_of_aoi(aois):
    result = []

    for aoi in aois:
        if aoi["kind"] == "sub-line":
            result.append(aoi["x"] + aoi["width"] / 2, aoi["y"] + aoi["heigth"])

def dist(x1, x2, y1, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def compute_disparity_of_fixation(fixation, centers):
    closest = None
    closest_distance = float("inf")


    for center in centers:
        distance = dist(fixation["x"], center["x"], fixation["y"], center["y"])
        if distance < closest_distance:
            closest_distance = distance
            closest = center

    return closest["x"] - fixation["x"], closest["y"] - fixation["y"]

def get_disparities(aois, fixations):
    centers = get_centers_of_aoi(aois)
    disparities = []
    for fixation in fixations:
        disparity_x, disparity_y = compute_disparity_of_fixation(fixation, centers)
        disparities.append((disparity_x, disparity_y))

def mean_shift(disparities, start_x, start_y, h):
    def sub_iteration(x, y):
        # compute weights =  gaussian (current center - points) ** 2
        weights = []
        weight_sum = 0
        for disparity in disparities:
            weight = (dist(disparity[0] - x, disparity[1] - y) / h)**2
            weights.append(weight)
            weight_sum += weight

        # compute weighted sum over x and y
        result_x, result_y = 0, 0
        for weight, disparity in zip(weights, disparities):
            result_x += weight / weight_sum * disparity[0]
            result_y += weight / weight_sum * disparity[1]

        return result_x, result_y
    
    TOLERANCE = h / 100

    x, y = start_x, start_y
    last_x, last_y = start_x, start_y
    new_x, new_y = sub_iteration(last_x, last_y)
    while dist(new_x, last_x, new_y, last_y) >= TOLERANCE:
        temp_x, temp_y = new_x, new_y
        new_x, new_y =  sub_iteration(new_x, new_y)
        last_x, last_y = temp_x, temp_y
    
    return new_x, new_y

def correction_mode_of_disparities(fixations, aois):
    disparities = get_disparities()
 
    H_ESTIMATE = (max(aois["width"]) -  min(aois["width"]) ** 2 + max(aois["heigth"]) -  min(aois["heigth"]) ** 2) ** 0.5
    iterations = 1
    TOLERANCE = H_ESTIMATE / 100
    
    last_x, last_y = mean_shift(disparities, 0, 0, H_ESTIMATE)
    new_x, new_y =  mean_shift(disparities, last_x, last_y, H_ESTIMATE)
    while dist(new_x, last_x, new_y, last_y) >= TOLERANCE:
        iterations += 1
        temp_x, temp_y = new_x, new_y
        new_x, new_y =  mean_shift(disparities, new_x, new_y, H_ESTIMATE / iterations)
        last_x, last_y = temp_x, temp_y

    new_fixations = []
    for fixation in fixations:
        fixation["x"] -= new_x
        fixation["y"] -= new_y
        new_fixations.append(fixation)
        
    return new_fixations