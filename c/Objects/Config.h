/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 * Implements a data structure to save and parse configaration options
 */

#ifndef XDCC_DOWNLOAD_CONFIG_H
#define XDCC_DOWNLOAD_CONFIG_H

#include "../Helpers/fileHandlers.h"

#include <string>
#include <vector>
#include <fstream>
#include <string.h>

using namespace std;

/**
 * The Config class that parses a config file and saves its properties as easily accesible variables
 */
class Config{

public:

    //Constructor
    Config(string ConfigFile);

    //Getter/Setter Functions
    string getServerFile();
    string getPackFile();

    string getHexChatCommand();

    string getScriptFileLocation();
    string getTextEditor();
    string getEmailAddress();
    string getEmailPassword();
    string getSmtpServer();
    string getSmtpPort();
    bool getEmailState();

private:

    //variables
    vector<string> fileContent;
    string serverFile;
    string packFile;
    string hexChatCommand;
    string scriptFileLocation;
    string textEditor;
    string emailAddress;
    string emailPassword;
    string smtpServer;
    string smtpPort;
    bool emailState;

    vector<string> defaults;
    vector<string> defaultServers;

    //helper functions
    void parse();
    void variableInit();

};

#endif //XDCC_DOWNLOAD_CONFIG_H
