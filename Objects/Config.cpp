/**
 * @author Hermann Krumrey hermann@krumreyh.com
 */

#include "Config.h"
#include <fstream>
#include <string.h>
#include <iostream>

using namespace std;

//Function implementations
//public

/**
 * Constructor
 * @param configFile - The location of the config file as a string
 */
Config::Config(string configFile){

    ifstream file(configFile);
    string line;
    vector<string> fileContent;

    while (getline(file, line)) {
        fileContent.push_back(line);
    }

    this->fileContent = fileContent;
    parse();
}

//Getter/Setter

string Config::getServerFile(){
    return this->serverFile;
}

string Config::getPackFile() {
    return this->packFile;
}

string Config::getTextEditor() {
    return this->serverFile;
}

bool Config::getEmailState() {
    return this->emailState;
}

vector<string> Config::getEmailSettings() {
    return this->emailSettings;
}


//private

void Config::parse() {

    string line;

    for (int i = 0; i < this->fileContent.size(); i++) {
        line = this->fileContent[i];
        if (!strncmp(line.c_str(), "#", 1)) { continue; } //Checks if the line is commented using a #
        else if (!strncmp(line.c_str(), "packfile=", 9)) { this->packFile = line.replace(0, 9, ""); }
        else if (!strncmp(line.c_str(), "serverfile=", 10)) { this->serverFile = line.replace(0, 10, ""); }
        else if (!strncmp(line.c_str(), "texteditor=", 10)) { this->textEditor = line.replace(0, 10, ""); }
        else if (!strncmp(line.c_str(), "sendemail=", 9)) {
            if (strcmp(line.c_str(), "sendemail=true")) {
                this->emailState = true;
            } else {
                this->emailState = false;
            }
        }
        else continue;
    } //runs in O(n) :D

}