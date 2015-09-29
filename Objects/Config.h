//
// Created by hermann on 9/29/15.
//

#ifndef XDCC_DOWNLOAD_CONFIG_H
#define XDCC_DOWNLOAD_CONFIG_H

#include <string>
#include <vector>

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
    vector<string> getEmailSettings();
    bool getEmailState();



private:

    //variables
    vector<string> fileContent;
    string serverFile;
    string packFile;
    string textEditor;
    bool emailState;
    vector<string> emailSettings;

    //functions
    void parse();

};

#endif //XDCC_DOWNLOAD_CONFIG_H
