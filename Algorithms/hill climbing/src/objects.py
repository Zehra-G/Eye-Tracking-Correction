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


class Distance(object):
    """
    Distance (Point, Point)
    CONSTRUCTION:
        set internal points to constructor params
        set distance to the distance between the points

    MEMBER VARIABLE(S):
    point1 Point
    point2 Point
    distance int/float - distance between point 1 and 2
    """
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.distance = (math.sqrt(math.pow(self.point2.x-self.point1.x, 2)))


class Aoi(object):
    """
    Aoi (str, str, int, int, int, int)
    CONSTRUCTION:
        set internal variable to the ones read from csv

    METHOD(S):
        bool containsPoint(int, int)
        PRECONDITION(S):
            given valid x and y ints
        POSTCONDITION(S):
            returns whether or not the given values are within the AOI rectangle

    MEMBER VARIABLE(S):
    kind str - type of AOI, line/subline
    name str - name of th aoi
    x int - top left x coordinate
    y int - top left y coordinate
    width int - width of rectangle
    height int - height of rectangle
    """
    def __init__(self, kind, name, x, y, width, height):
        self.kind = kind
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def containsPoint(self, pointx, pointy):
        if pointx > self.x and pointx < (self.x + self.width):
            if pointy > self.y and pointy < (self.y + self.width):
                return True
        return False
#    def contains_point(self, point):


class Point(object):
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


class SessionsOfPoints:
    """
    SessionsOfPoints ()
    CONSTRUCTION:
        create empty dict container for listOfFiles

    METHOD(S):
    <estimated return type> <method name> (<params>)
    None add_session(list[Point], str)
    PRECONDITION(S):
        filename str is a valid filename
    POSTCONDITION(S):
        listOfFiles maps the filename to the list[points] given

    list[Point] get_session(str)
    PRECONDITION(S):
        the given str filename is a valid key in listOfFiles
    POSTCONDITION(S):
        return listOfFiles[filename]

    int get_number_of_sessions()
    PRECONDITION(S):
        None
    POSTCONDITION(S):
        return the number of sessions in listOfFiles

    MEMBER VARIABLE(S):
    listOfFiles list[Point]
    """
    def __init__(self):
        self.listOfFiles = {}

    def add_session(self, session, filename):
        self.listOfFiles[filename] = session

    def get_session(self, filename):
        return self.listOfFiles[filename]

    def get_number_of_sessions(self):
        return len(self.listOfFiles)


class FileOfClusters:
    """
    FileOfClusters ()
    CONSTRUCTION:

    METHOD(S):
    None add_cluster(list[Point], str)
        sets clusterdict[filename equal to list[point] (cluster)

    list[Point] get_cluster(str)
        returns list[point] from given key

    int get_number_of_clusters()
        returns the number of clusters

    MEMBER VARIABLE(S):
    clusterDict dict{filename: list[Point]}
    """
    def __init__(self):
        self.clusterDict = {}

    #todo this should probably append not assign
    def add_cluster(self, cluster, filename):
        self.clusterDict[filename] = cluster

    def get_cluster(self, filename):
        return self.clusterDict[filename]

    def get_number_of_clusters(self):
        number_of_clusters = 0
        for i in self.clusterDict:
            number_of_clusters += len(i)
        return number_of_clusters / len(self.clusterDict)
