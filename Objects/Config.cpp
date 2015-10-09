/**
 * @author Hermann Krumrey hermann@krumreyh.com
 * Implements a data structure to save and parse configaration options
 */

#include <iostream>
#include "Config.h"

//Function implementations
//public

/**
 * Constructor
 * @param configFile - The location of the config file as a string
 */
Config::Config(string configFile){

    variableInit();

    //Checks if Config File exits. If not, a default config file is generated
    try {
        this->fileContent = readFile(configFile);
    } catch (int e) {
        if (e == 404) {
            string command1 = "mkdir /home/" + string(getenv("USER")) + "/.xdcc-download";
            string command2 = "mkdir /home/" + string(getenv("USER")) + "/.xdcc-download/files";
            system(command1.c_str());
            system(command2.c_str());
            writeToFile(configFile, this->defaults);
            this->fileContent = this->defaults;
        }
    }
    parse();

    //Checks if pack/serverfile exists and generates them if not.
    if (!isFile(this->packFile)) {
        writeToFile(this->packFile, {"#Packfile"});
    }
    if (!isFile(this->serverFile)) {
        writeToFile(this->serverFile, this->defaultServers);
    }
}

//Getter/Setter

string Config::getServerFile(){
    return this->serverFile;
}

string Config::getPackFile() {
    return this->packFile;
}

string Config::getHexChatCommand() {
    return this->hexChatCommand;
}

string Config::getScriptFileLocation() {
    return this->scriptFileLocation;
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

/**
 * Parses the config file and saves the information as local variables
 */
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
        else if (!strncmp(line.c_str(), "hexchat-command=", 16)) { this->hexChatCommand = line.replace(0, 16, ""); }
        else if (!strncmp(line.c_str(), "script-file-location=", 21)) {
            this->scriptFileLocation = line.replace(0, 21, "");
        }
        else continue;
    }

}

/**
 * Initializes the private variables needed by the class to function correctly
 */
void Config::variableInit() {

    this->emailState = false;

    this->defaults = {"#Default Config File",
                      "packfile=/home/" + string(getenv("USER")) + "/.xdcc-download/files/packfile",
                      "serverfile=/home/" + string(getenv("USER")) + "/.xdcc-download/files/serverfile",
                      "hexchat-command=hexchat",
                      "script-file-location=/home/" + string(getenv("USER")) +
                      "/.config/hexchat/addons/xdcc-download.py",
                      "texteditor=gedit",
                      "sendemail=false",
                      "email-address=user@server.domain",
                      "email-password=p455w0RDg035H34R",
                      "smtp-server=smtp.server.domain",
                      "smtp-port=999"};

    this->defaultServers = {"#Serverfile\n",
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
}