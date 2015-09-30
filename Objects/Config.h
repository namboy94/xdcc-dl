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
    string textEditor;
    string emailAddress;
    string emailPassword;
    string smtpServer;
    string smtpPort;
    bool emailState = false;

    vector<string> defaults = {"#Default Config File",
                               "packfile=",
                               "serverfile=",
                               "texteditor=",
                               "sendemail=false",
                               "email-address=user@server.domain",
                               "email-password=p455w0RDg035H34R",
                               "smtp-server=smtp.server.domain",
                               "smtp-port=999"};//TODO How to get username etc.

    //helper functions
    void parse();

};

#endif //XDCC_DOWNLOAD_CONFIG_H
