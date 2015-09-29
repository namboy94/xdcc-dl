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

bool isFile(string file);
vector<string> readFile(string file);
void createFile(string file);
void writeToFile(string file, vector<string> content);


#endif //XDCC_DOWNLOAD_FILEHANDLERS_H
