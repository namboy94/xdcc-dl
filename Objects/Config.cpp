/**
 * @author Hermann Krumrey hermann@krumreyh.com
 * Implements a data structure to save and parse configaration options
 */

#include "Config.h"

//Function implementations
//public

/**
 * Constructor
 * @param configFile - The location of the config file as a string
 */
Config::Config(string configFile){

    try {
        this->fileContent = readFile(configFile);
    } catch (int e) {
        if (e == 404) {
            writeToFile(configFile, defaults);
            this->fileContent = readFile(configFile);
        }
    }
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
    return this->textEditor;
}

bool Config::getEmailState() {
    return this->emailState;
}

string Config::getEmailAddress() {
    return this->emailAddress;
}

string Config::getEmailPassword() {
    return this->emailPassword;
}

string Config::getSmtpServer() {
    return this->smtpServer;
}

string Config::getSmtpPort() {
    return this->smtpPort;
}

//private

void Config::parse() {

    string line;

    for (int i = 0; i < this->fileContent.size(); i++) {
        line = this->fileContent[i];
        if (!strncmp(line.c_str(), "#", 1)) { continue; } //Checks if the line is commented using a #
        else if (!strncmp(line.c_str(), "packfile=", 9)) { this->packFile = line.replace(0, 9, ""); }
        else if (!strncmp(line.c_str(), "serverfile=", 11)) { this->serverFile = line.replace(0, 11, ""); }
        else if (!strncmp(line.c_str(), "texteditor=", 11)) { this->textEditor = line.replace(0, 11, ""); }
        else if (!strncmp(line.c_str(), "email-address=", 14)) { this->emailAddress = line.replace(0, 14, ""); }
        else if (!strncmp(line.c_str(), "email-password=", 15)) { this->emailPassword = line.replace(0, 15, ""); }
        else if (!strncmp(line.c_str(), "smtp-server=", 12)) { this->smtpServer = line.replace(0, 12, ""); }
        else if (!strncmp(line.c_str(), "smtp-port=", 10)) { this->smtpPort = line.replace(0, 10, ""); }
        else if (!strncmp(line.c_str(), "sendemail=true", 14)) { this->emailState = true; }
        else continue; //Empty or un-parseable line;
    } //runs in O(n) :D

}