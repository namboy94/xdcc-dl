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


#endif //XDCC_DOWNLOAD_FILEHANDLERS_H
