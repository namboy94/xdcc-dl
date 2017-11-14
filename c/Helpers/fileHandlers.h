/*
Copyright 2015-2017 Hermann Krumrey

This file is part of xdcc-downloader.

xdcc-downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xdcc-downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xdcc-downloader.  If not, see <http://www.gnu.org/licenses/>.
*/

/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 * Collection of methods to help with processing files
 */

#ifndef XDCC_DOWNLOAD_FILEHANDLERS_H
#define XDCC_DOWNLOAD_FILEHANDLERS_H

#include <string>
#include <fstream>
#include <vector>

using namespace std;


//Declarations

bool isFile(string file);                                   //Checks if a file exists
vector<string> readFile(string file);                       //Reads a file and returns it as a vector of strings, which
                                                            // may be handled similarly to an array
vector<string> readFileNoHash(string file);                 //Reads a file and returns it as a vector of strings, which
                                                            // may be handled similarly to an array.
                                                            //Lines starting with # symbols are ommited
void createFile(string file);                               //Creates a new, empty file.
void writeToFile(string file, vector<string> content);      //Writes a vector of Strings to a newline seperated textfile
void appendLine(string line, string file);                  //Appends a line to a text file
void deleteFile(string file);                               //Deletes a file


#endif //XDCC_DOWNLOAD_FILEHANDLERS_H
