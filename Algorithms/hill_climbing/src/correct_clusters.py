"""
This file is part of Fixation-Correction-Sourcecode.

Fixation-Correction-Sourcecode is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

Fixation-Correction-Sourcecode is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Fixation-Correction-Sourcecode.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2015
Author: Chris Palmer
"""

import pandas as pd



def correct_cluster(listofclusters, listofaois):
    """
    None correct_cluster(list[list[point]], list[AOI])
    PRECONDITION(S):
        given a list[list[point]] (list of clusters) and a list of AOIs
        Point has the properties:
            -autoxCorrected - the x coordinate of a point that has been corrected automatically
            -autoyCorrected - the y coordinate of a point that has been corrected automatically

            -x - original x coordinate of a point
            -y - original y coordinate of a point

    POSTCONDITION(S):
        all autoCorrect points in the list[list[point]] are set to the value of their original points
        if a cluster in the list[list[]] scores 0 from the scoring function
            the cluster is moved toward the nearest aoi

        hillclimb is called on the current state of each cluster

        note: all passes are done by reference
    """
    listofaois = listofaois.values.tolist()
    for cluster in listofclusters:
        for point in cluster:
            point.append(point[0])
            point.append(point[1])
        if find_score_multi_aoi(cluster, listofaois) == 0:
            move_cluster_toward_aoi(cluster, listofaois)

        hillclimb(cluster, listofaois)
        
        
                
    return listofclusters


def find_score_multi_aoi(cluster, listofaois):
    """
    float find_score_multi_aoi (list[point], list[AOI])
    PRECONDITION(S):
        given a list of points and a list of AOIs
    POSTCONDITION(S):
        return the number of points in an aoi / the number of points in the cluster
    """
    list_of_points_in_aoi = []
    debug_points = []
    for point in cluster:
        if debug_points.count(point) > 0:
            # todo throw an exception?
            print ("point repeat error")
        debug_points.append(point)

        for aoi in listofaois:
            if point_in_aoi(point, aoi):
                if list_of_points_in_aoi.count(point) == 0:
                    list_of_points_in_aoi.append(point)

    return float(len(list_of_points_in_aoi))/float(len(cluster))


def point_in_aoi(point, aoi):
    """
    bool point_in_aoi(Point, AOI)
    PRECONDITION(S):
        given a valid Point and AOI
        Point has properties:
            -autoxCorrected
            -autoyCorrected

        AOI has properties:
            -x - the top left x coordinate of AOI
            -y - the top left y coordinate of AOI
            -width - the width in pixels of AOI
            -height - the height in pixels of AOI

    POSTCONDITION(S):
        return True if the point is within the defined AOI rectangle
        return False if the point is not within the AOI rectangle
    """
    if point[5] >= aoi[2] and point[5] <= (aoi[2] + aoi[4]):
        if point[6] >= aoi[3] and point[6] <= (aoi[3] + aoi[5]):
            return True
        else:
            return False
    return False
# def find_score_single_aoi(cluster, aoi):


def hillclimb(cluster, listofaois):
    """
    None hillclimb (list[Point], list[AOI])
    Driver funtion for hillclimb algorithm
    PRECONDITION(S):
        given a list of Points and a list of AOIs
        move distance starts at the size of the AOI rectangle for vert/hor distances

    POSTCONDITION(S):
        the x and y autoCorrect values for each point will be changed to the highest scoring values
        that the hillclimbing algorithm can acheive

        note: all values are passed by reference
    """
    movevertdistance = get_maxY(cluster) - get_minY(cluster)
    movehordistance = get_maxX(cluster) - get_minX(cluster)

    hillclimbloop = 0

    shift_dir(cluster, 'left', movehordistance)
    left = find_score_multi_aoi(cluster, listofaois)

    shift_dir(cluster, 'right', movehordistance)
    shift_dir(cluster, 'right', movehordistance)
    right = find_score_multi_aoi(cluster, listofaois)

    shift_dir(cluster, 'left', movehordistance)
    shift_dir(cluster, 'up', movevertdistance)
    up = find_score_multi_aoi(cluster, listofaois)

    shift_dir(cluster, 'down', movevertdistance)
    shift_dir(cluster, 'down', movevertdistance)
    down = find_score_multi_aoi(cluster, listofaois)

    shift_dir(cluster, 'up', movevertdistance)
    current = find_score_multi_aoi(cluster, listofaois)

    while movevertdistance >= 1 or movehordistance >= 1:
        while current < left or current < right or current < up or current < down:
            hillclimbloop += 1
            # print("hillclimb loop " + str(hillclimbloop))
            if left > current:
                shift_dir(cluster, 'left', movehordistance)
            elif right > current:
                shift_dir(cluster, 'right', movehordistance)
            elif up > current:
                shift_dir(cluster, 'up', movevertdistance)
            elif down > current:
                shift_dir(cluster, 'down', movevertdistance)

            shift_dir(cluster, 'left', movehordistance)
            left = find_score_multi_aoi(cluster, listofaois)

            shift_dir(cluster, 'right', movehordistance)
            shift_dir(cluster, 'right', movehordistance)
            right = find_score_multi_aoi(cluster, listofaois)

            shift_dir(cluster, 'left', movehordistance)
            shift_dir(cluster, 'up', movevertdistance)
            up = find_score_multi_aoi(cluster, listofaois)

            shift_dir(cluster, 'down', movevertdistance)
            shift_dir(cluster, 'down', movevertdistance)
            down = find_score_multi_aoi(cluster, listofaois)

            shift_dir(cluster, 'up', movevertdistance)
            current = find_score_multi_aoi(cluster, listofaois)

        movevertdistance = int(movevertdistance/2)
        movehordistance = int(movehordistance/2)
    return


def shift_dir(cluster, direction, distance):
    """
    None shift_dir(list[Point], str, int)
    PRECONDITION(S):
        Point has properties:
            -autoxCorrected - x coordinate of auto corrected fixation
            -autoyCorrected - y coordinate of auto corrected fixation

    POSTCONDITION(S):
        all points in cluster are shifted in the direction of str
        the distance defined in the int
    """
    if direction == 'left':
        for point in cluster:
            point[5] -= distance

    if direction == 'right':
        for point in cluster:
            point[5] += distance

    if direction == 'up':
        for point in cluster:
            point[6] -= distance

    if direction == 'down':
        for point in cluster:
            point[6] += distance

    return


def move_cluster_toward_aoi(cluster, listofaois):
    """
    None move_cluster_toward_aoi (list[Point], list[AOI])
    PRECONDITION(S):
        given list of Points and list of AOIs

    POSTCONDITION(S):
        The cluster of points will be moved to the nearest AOI until at least 1 point is contained in it
    """
    nearestaoi = find_nearest_aoi(cluster, listofaois)
    while find_score_multi_aoi(cluster, listofaois) == 0:
        moved = False
        if nearestaoi[2] < get_minX(cluster):
            #print('left')
            shift_dir(cluster, 'left', 1)
            moved = True
        elif nearestaoi[2] > get_minX(cluster):
            #print('right')
            shift_dir(cluster, 'right', 1)
            moved = True
        if nearestaoi[3] < get_minY(cluster):
            #print('up')
            shift_dir(cluster, 'up', 1)
            moved = True
        elif nearestaoi[3] > get_minY(cluster):
            #print('down')
            shift_dir(cluster, 'down', 1)
            moved = True
        if moved:
            break


# todo make cluster class these would be methods in that class
def get_maxX(cluster):
    """
    int get_maxX(list[Point])
    PRECONDITION(S):
        Point has properties:
            -autoxCorrected
    POSTCONDITION(S):
        return the largest autoxCorrected value in cluster
    """
    maxX = 0
    for point in cluster:
        if point[5] > maxX:
            maxX = point[5]
    return maxX


def get_maxY(cluster):
    """
    int get_maxY(list[Point])
    PRECONDITION(S):
        Point has properties:
        -autoyCorrected
    POSTCONDITION(S):
        return the largest autoyCorrect value
    """
    maxY = 0
    for point in cluster:
        if point[6] > maxY:
            maxY = point[6]
    return maxY


def get_minX(cluster):
    """
    int get_minX(list[Point])
    PRECONDITION(S):
        Point has properties:
            -autoxCorrected
    POSTCONDITION(S):
        retuen the smallest autoxCorrected value
    """
    minX = cluster[0][0]
    for point in cluster:
        if point[5] < minX:
            minX = point[5]
    return minX


def get_minY(cluster):
    """
    int get_minY(list[Point])
    PRECONDITION(S):
        Point has the properties:
            -autoyCorrected
    POSTCONDITION(S):
        return the smallest autoyCorrected value in cluster
    """
    minY = cluster[0][1]
    for point in cluster:
        if point[6] < minY:
            minY = point[6]
    return minY


def find_nearest_aoi(cluster, listofaois):
    """
    AOI find_nearest_aoi(list[Point], list[AOI])
    PRECONDITION(S):
        AOI has properties:
            -x
            -y
    POSTCONDITION(S):
        returns the AOI that is closest to the cluster
    """
    maxX = get_maxX(cluster)
    maxY = get_maxY(cluster)
    minX = get_minX(cluster)
    minY = get_minY(cluster)
    nearestaoi = listofaois[0]
    for i in range(1, len(listofaois)):
        if abs(listofaois[i][2] - minX) < abs(nearestaoi[2] - minX) and abs(listofaois[i][3] - minY) < abs(nearestaoi[3] - minY):
            nearestaoi = listofaois[i]

    return nearestaoi