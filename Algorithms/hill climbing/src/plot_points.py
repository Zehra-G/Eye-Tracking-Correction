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

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import globalVariables


def plot_points(listofpoints, filename, listofaois):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    for point in listofpoints:
        plt.plot(point.x, -point.y, 'bo', label=filename)
    plt.savefig('point-plots/'+filename+'.png')


def plot_aois(listofaois, filename, list_of_clusters):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    numerOfAois = 0
    print globalVariables.AOI_FILES[filename]
    for aoi in listofaois:
        for cluster in list_of_clusters:
            for point in cluster:
                plt.plot(point.x, -point.y, 'bo')
        rectangle = Rectangle((aoi.x, -aoi.y), aoi.width, aoi.height, fc='r')
        numerOfAois += 1
        plt.gca().add_patch(rectangle)
    print(str(numerOfAois) + ' aois')

    period = filename.rfind('.')
    filename = filename[:-(len(filename)-period)]

    print(str(len(list_of_clusters)) + ' clusters')
    if len(list_of_clusters) > 0:
        plt.savefig('aoi-plots/' + filename)
    plt.clf()
    plt.close('all')
    #----------------------------------------------------------------------------------
    numerOfAois = 0
    autocorrected = False
    for cluster in list_of_clusters:
        for point in cluster:
            if point.x != point.autoxCorrected or point.y != point.autoyCorrected:
                autocorrected = True
    if autocorrected:
        for aoi in listofaois:
            for cluster in list_of_clusters:
                for point in cluster:
                    plt.plot(point.autoxCorrected, -point.autoyCorrected, 'ro')
            rectangle = Rectangle((aoi.x, -aoi.y), aoi.width, aoi.height, fc='g')
            numerOfAois += 1
            plt.gca().add_patch(rectangle)
        print(str(numerOfAois) + ' aois')

        print(str(len(list_of_clusters)) + ' clusters')
        if len(list_of_clusters) > 0:
            plt.savefig('aoi-plots/' + filename+"_autocorrected")
        plt.clf()
        plt.close('all')
    return len(list_of_clusters)
    # plt.show()
