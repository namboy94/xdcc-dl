/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 * Collection of methods to help with processing files
 */

#include <string.h>
#include "fileHandlers.h"


//Implementations

/*
 * Checks if a file exists
 * @param file - the path of the file to be checked
 */
bool isFile(string file) {
    ifstream input(file);
    if (input) {
        input.close();
        return true;
    } else {
        input.close();
        return false;
    }
}

/*
 * Reads a file and returns it as a vector of strings, which may be handled similarly to an array
 * @param file - the path of the file to be read
 * @throws 404 if the file is not found
 */
vector<string> readFile(string file) {

    vector<string> fileContent;

    if (!isFile(file)) {
        throw 404;
    }
    ifstream input(file);
    string line;

    while (getline(input, line)) {
        fileContent.push_back(line);
    }

    return fileContent;
}

/*
 * Reads a file and returns it as a vector of strings, which may be handled similarly to an array
 * Lines starting with # symbols are ommited
 * @param file - the path of the file to be read
 * @throws 404 if the file is not found
 */
vector<string> readFileNoHash(string file) {

    vector<string> fileContent;

    if (!isFile(file)) {
        throw 404;
    }
    ifstream input(file);
    string line;

    while (getline(input, line)) {
        if (!strncmp(line.c_str(), "#", 1)) { continue; }
        fileContent.push_back(line);
    }

    return fileContent;
}


/**
 * Creates a new, empty file.
 * @param file - the path to the file to be created
 * @throws 503 if the file already exists
 */
void createFile(string file) {
    if (isFile(file)) { throw 503; }
    ofstream output(file);
    output.close();
}

void deleteFile(string file) {
    remove(file.c_str());
}

/**
 * Writes a vector of Strings to a newline seperated textfile
 * @param file - the path of the file to be written to
 * @param content - the content to be written to the file
 * @throws 503 if the file already exists
 */
void writeToFile(string file, vector<string> content) {
    deleteFile(file);
    createFile(file);
    ofstream output(file);
    for (int i = 0; i < content.size(); i++) {
        string line = content[i] + "\n";
        output.write(line.c_str(), content[i].size() + 1);
    }
    output.close();
}