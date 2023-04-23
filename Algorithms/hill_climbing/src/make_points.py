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

import objects
import globalVariables
import csv


def make_points():
    """
    dict{filename: list[Point]} make_points()
    PRECONDITION(S):
        globalVariables.files is a list of filenames
    POSTCONDITION(S):
        return dict of list of points by filename
    """
    dict_of_points = {}

    for filename in globalVariables.files:
        dict_of_points[filename] = create_list_of_points(filename)

    return dict_of_points


def create_list_of_points(filename):
    """
    list[Point] create_list_of_points(str)
    PRECONDITION(S):
        the string is a valid filename
    POSTCONDITION(S):
        return a list[Point] of Points generated from the given filename
    """
    # variables
    point_list = []
    data_folder = "eye-tracking-data/"
    filename_path = data_folder+filename

    with open(filename_path) as data_csv_file:
        reader = csv.DictReader(data_csv_file)

        for row in reader:
            point_list.append(objects.Point(int(row['fix_x_original']),           int(row['fix_y_original']),           int(row['duration_ms']),
                                            int(row['start_ms']),        int(row['end_ms']),          str(row['aoi_sub.line']),
                                            int(row['fix_x']), int(row['fix_y']), filename))

    return point_list
