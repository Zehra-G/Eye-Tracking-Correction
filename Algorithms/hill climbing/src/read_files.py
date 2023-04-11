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

from os import walk
files = []


def read(directory_of_files):
    """
    <estimated return type> <function_name> (<parameters>)
    PRECONDITION(S):
    POSTCONDITION(S):
    """
    for (dirpath, dirnames, filenames) in walk(directory_of_files):
        files.extend(filenames)
        break
    for name in files:
        if ".csv" not in name:
            files.remove(name)
    return files