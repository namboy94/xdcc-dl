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
                               "packfile=/home/" + string(getenv("USER")) + "/.xdcc-download/files/packfile",
                               "serverfile=/home/" + string(getenv("USER")) + "/.xdcc-download/files/serverfile",
                               "texteditor=gedit",
                               "sendemail=false",
                               "email-address=user@server.domain",
                               "email-password=p455w0RDg035H34R",
                               "smtp-server=smtp.server.domain",
                               "smtp-port=999"};

    vector<string> defaultServers = {"#Serverfile\n",
                                     "#Rizon",
                                     "##horriblesubs",
                                     "Ginpachi-Sensei @ rizon/horriblesubs",
                                     "CR-TEXAS|NEW @ rizon/horriblesubs",
                                     "CR-TEXAS2|NEW @ rizon/horriblesubs",
                                     "CR-HOLLAND|NEW @ rizon/horriblesubs",
                                     "CR-GERMANY|NEW @ rizon/horriblesubs",
                                     "CR-GERMANY2|NEW @ rizon/horriblesubs",
                                     "CR-FRANCE|NEW @ rizon/horriblesubs",
                                     "CR-CANADA|NEW @ rizon/horriblesubs",
                                     "CR-ASIA|NEW @ rizon/horriblesubs",
                                     "CR-ARUTHA|720p @ rizon/horriblesubs",
                                     "CR-ARCHIVE|SD @ rizon/horriblesubs",
                                     "CR-ARCHIVE|720p @ rizon/horriblesubs",
                                     "CR-ARCHIVE|1080p @ rizon/horriblesubs",
                                     "Arutha|DragonBall @ rizon/horriblesubs",
                                     "##Doki",
                                     "Doki|Homura @ rizon/doki",
                                     "Doki|Misaki @ rizon/doki",
                                     "Doki|Michiko @ rizon/doki",
                                     "Doki|Kyou @ rizon/doki",
                                     "Doki|Nanoha @ rizon/doki",
                                     "Doki|Fate @ rizon/doki",
                                     "Doki|Kobato @ rizon/doki",
                                     "Doki|s2 @ rizon/doki",
                                     "Doki|s3 @ rizon/doki",
                                     "Doki|s4 @ rizon/doki",
                                     "Doki|s5 @ rizon/doki",
                                     "##exiled-destiny",
                                     "E-D|Mashiro @ rizon/exiled-destiny",
                                     "##news",
                                     "NIBL|Abraham @ rizon/news",
                                     "NIBL|Arutha @ rizon/news",
                                     "NIBL|Asian @ rizon/news",
                                     "NIBL|Asuka @ rizon/news",
                                     "NIBL|Deadpool @ rizon/news",
                                     "NIBL|Erza @ rizon/news",
                                     "NIBL|Hentai @ rizon/news",
                                     "NIBL|Ippo @ rizon/news",
                                     "NIBL|Issei @ rizon/news",
                                     "NIBL|Konata @ rizon/news",
                                     "NIBL|Onizuka @ rizon/news",
                                     "NIBL|Ragnar @ rizon/news",
                                     "NIBL|Ray @ rizon/news",
                                     "NIBL|Satella @ rizon/news",
                                     "NIBL|Walter @ rizon/news",
                                     "NIBL|Yomiko @ rizon/news",
                                     "NIBL|Zed @ rizon/news"};

    //helper functions
    void parse();

};

#endif //XDCC_DOWNLOAD_CONFIG_H
