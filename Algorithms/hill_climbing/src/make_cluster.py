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

import math
import numpy 

class Point():
    """
    Point (int, int, int, int, int, str, int, int, str)
    CONSTRUCTION:
        set internal variables to param values

    METHOD(S):
        bool/float xCorrectionCoefficient()
        PRECONDITION(S):
            xCorrected != x

        POSTCONDITION(S):
            return (xautocorrected-x)/(xCorrected-x)

        bool/float yCorrectionCoefficient()
        PRECONDITION(S):
            yCorrected != y
        POSTCONDITION(S):
            return (yautocorrected-y)/(yCorrected-y)

    MEMBER VARIABLE(S):
        x int - the original x coordinate of fixation point
        y int - the original y coordinate of fixation point
        duration int - the time ms? spent on that fixation
        startTime int - the start time ms? of the fixation point
        endTime int - the end time ms? of the fixation point
        aoi str - the type of aoi that the point is associated with line/subline can be None
        xCorrected int - manually corrected x coordinate
        yCorrected int - manually corrected y coordinate
        filename str - name of the file for fixation data
        autoxCorrected int - auto corrected x coordinate
        autoyCorrected int - auto corrected y coordinate
    """
    def __init__(self, x, y, duration, startTime, endTime, aoi, xCorrected, yCorrected, filename):
        self.x = x
        self.y = y
        self.duration = duration
        self.startTime = startTime
        self.endTime = endTime
        self.aoi = aoi
        self.xCorrected = xCorrected
        self.yCorrected = yCorrected
        self.filename = filename
        self.autoxCorrected = None
        self.autoyCorrected = None

    def xCorrectionCoefficient(self):
        if not self.autoxCorrected:
            return (self.autoxCorrected-self.x)/(self.xCorrected-self.x)
        else:
            return False

    def yCorrectionCoeffieient(self):
        if not self.autoyCorrected:
            return (self.autoyCorrected-self.y)/(self.yCorrected-self.y)
        else:
            return False
        

# global variable(s)

NUMBER_OF_ELEMENTS_TO_REMOVE = 0

# function to check if object exists in list

def make_points(fixations):
    
    fixations = fixations.tolist()
    start = 0
    end = 0
    for i in range(len(fixations)):
        fixations[i].append(start)
        end = fixations[i][2] + start
        fixations[i].append(end)
        start = end
        
    point_list = []
    for point in fixations:
        point_list.append(Point(point[0], point[1], point[2], point[3], point[4], None, None, None, None))
        
           
    return point_list


def make_one_cluster_per_file(listOfPoints):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    returnList = []
    returnList.append(listOfPoints)
    return returnList


def make_one_cluster_per_point(listOfPoints):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    returnList = []
    for point in listOfPoints:
        returnList.append([point])

    return returnList


def contains(list, filter):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    for x in list:
        if filter(x):
            return True
    return False


def median(lst):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    return numpy.median(numpy.array(lst))


def create_cluster(sessionpoints):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    # sessionpoints is a list of points
    print("create cluster method")


# Take list of points
# Return list of clusters
def make_cluster_refactor(listOfPoints):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    # variables
    # lookbackQueue[0]  = oldest element
    # lookbackQueue[-1] = newest element
    
    
    lookbackQueue = []
    listOfClusters = []
    listOfPoints = make_points(listOfPoints)
    totalMedian = find_median(listOfPoints)
    lookbackQueueInitialized = False
    firstLoop = True
    output = open('overflowlog.txt', 'w')
    
    

    for point in listOfPoints:
        # Initialize the queue as full
        if not lookbackQueueInitialized:
            if firstLoop:
                lookbackQueue.append(point)
                firstLoop = False

            else:
                lookbackQueue.append(point)
                if lookbackQueue[-1].startTime - lookbackQueue[0].startTime < 15000:
                    continue
                else:
                    lookbackQueueInitialized = True

        # todo ponder the questionable nature of possibly losing a point
        # maybe check for clusters during initalization
        else:
            while lookbackQueue[-1].startTime - lookbackQueue[0].startTime > 15000:
                lookbackQueue.pop(0)
            if check_if_cluster_too_big(lookbackQueue, totalMedian):
                # todo ouput to log file
                for each in lookbackQueue:
                    output.write(str(each.startTime) + '\n')
                output.write('\n')
                if find_distance(lookbackQueue[-1], lookbackQueue[-2]) >= totalMedian:
                    # clear the queue except for the newest point
                    for i in range(0, len(lookbackQueue)-1):
                        lookbackQueue.pop(i)
                else:
                    lookbackQueue = []
                    lookbackQueueInitialized = False

            elif check_for_cluster(lookbackQueue, totalMedian):
                cluster = extract_cluster(lookbackQueue, totalMedian)
                if cluster is not None:
                    listOfClusters.append(cluster)

                for i in range(0, NUMBER_OF_ELEMENTS_TO_REMOVE):
                    if i < len(lookbackQueue):
                        lookbackQueue.pop(i)
                # lookbackQueue = [] #todo correct this to only remove the cluster points
                lookbackQueueInitialized = False

            # else there is a cluster in progress. Do nothing. Move along. These aren't the droids you're looking for
    print("Iiiiiiiiiiiiiiiiiiiiiiiiiiiii")

    return listOfClusters



    # this is pseudocode
    #
    # find the    median distance between all points
    # for point in listOfPoints
    # {
    #   push points to lookback queue
    #   keep queue appropriate size
    #   if not clusteroverflow
    #     {
    #     if there is a cluster(group of temporally neighboring points with distance < median) in the queue
    #         {
    #             extract the cluster and clear any older points
    #             append cluster to list of clusters
    #             clear cluster
    #         }
    #     else if the cluster was too big
    #         {
    #         set clusteroverflow flag
    #         }
    #   else if clusteroverflow flag is set
    #     {
    #         if distance between newest and 2nd newest points >= median
    #             clear queue except for newest point
    #             unset clusteroverflow flag
    #     }
    # }

# refactor using find_distance()

def find_median(listOfPoints):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    pointDistances = []

    for i in range(1, len(listOfPoints)):
        point1x = int(listOfPoints[i].x)
        point1y = int(listOfPoints[i].y)
        point2x = int(listOfPoints[i-1].x)
        point2y = int(listOfPoints[i-1].y)

        distance = math.sqrt(math.pow(point2x-point1x, 2) +
                             math.pow(point2y-point1y, 2))

        pointDistances.append(distance)
    minimum = min(pointDistances)
    maximum = max(pointDistances)

    if .175 > 0:
        return numpy.median(numpy.array(pointDistances)) + (0.175 * (maximum - numpy.median(numpy.array(pointDistances))))
    elif 0.175 < 0:
        return numpy.median(numpy.array(pointDistances)) - (0.175 * (numpy.median(numpy.array(pointDistances)) - minimum))
    else:
        return numpy.median(numpy.array(pointDistances))


def find_distance(point1, point2):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    return math.sqrt(math.pow(int(point2.x - point1.x), 2) +
                     math.pow(int(point2.y - point1.y), 2))


# take queue and median distance as parameter and return boolean of whether or not there is a cluster in the queue
# only return true if there is an extractable cluster
def check_for_cluster(lookbackQueue, totalMedian):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    clusterSize = 0
    for i in range(1, len(lookbackQueue)):
        if i == len(lookbackQueue):
            if find_distance(lookbackQueue[i], lookbackQueue[i-1]) < totalMedian:
                return False
        if find_distance(lookbackQueue[i], lookbackQueue[i-1]) < totalMedian:
            clusterSize += 1
        else:
            if clusterSize >= 3:
                return True
            else:
                clusterSize = 0

    return False


# take queue as input return cluster from inside the queue
def extract_cluster(lookbackQueue, totalMedian): # todo reread this
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    global NUMBER_OF_ELEMENTS_TO_REMOVE
    NUMBER_OF_ELEMENTS_TO_REMOVE = 0
    cluster = []
    firstLoop = True
    for i in range(1, len(lookbackQueue)):
        if lookbackQueue[i].startTime - lookbackQueue[i-1].startTime < totalMedian:
            if firstLoop:
                cluster.append(lookbackQueue[i-1])
                cluster.append(lookbackQueue[i])
                firstLoop = False
            else:
                cluster.append(lookbackQueue[i])

    if len(cluster) >= 3:
        NUMBER_OF_ELEMENTS_TO_REMOVE = len(cluster)
        return cluster
    return


# if all the points are less than median distance apart return, if so return true
def check_if_cluster_too_big(lookbackQueue, totalMedian):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    tooBig = True
    for i in range(1, len(lookbackQueue)):
        if lookbackQueue[i].startTime - lookbackQueue[i-1].startTime >= totalMedian:
            tooBig = False
    if tooBig:
        print("too big")
    return tooBig
