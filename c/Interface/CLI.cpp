/*
Copyright 2015-2017 Hermann Krumrey

This file is part of xdcc-downloader.

xdcc-downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xdcc-downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xdcc-downloader.  If not, see <http://www.gnu.org/licenses/>.
*/

/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include <iostream>
#include "CLI.h"

CLI::CLI(HexChatPythonDownloader downloader, Config config) {

    variableInit();
    this->downloader.push_back(downloader);
    this->config.push_back(config);

}

void CLI::mainLoop() {

    cout << "XDCC-Download by Hermann Krumrey\n\n";
    bool running = true;

    while (running) {
        cout << "What would you like to do?\n";
        string input;
        getline(cin, input);

        if (!strcmp(input.c_str(), "quit")) {
            running = false;
        } else if (!strcmp(input.c_str(), "edit packs")) {
            this->downloader[0].editPacks();
        } else if (!strcmp(input.c_str(), "edit servers")) {
            this->downloader[0].editServers();
        } else if (!strcmp(input.c_str(), "start")) {
            this->downloader[0].downloadAll();
        } else if (regex_match(input, regex("/msg (\\S)+ xdcc send #[0-9]+"))) {
            this->downloader[0].downloadSinglePack(input);
        } else if (regex_match(input, regex("add /msg (\\S)+ xdcc send #[0-9]+"))) {
            this->downloader[0].addSinglePack(input);
        } else if (regex_match(input, regex("add (\\S)+ @ (\\S)+/(\\S)+"))) {
            this->downloader[0].addSingleBot(input);
        } else if (!strcmp(input.c_str(), "print")) {
            this->downloader[0].printPacks();
        } else if (!strcmp(input.c_str(), "print all")) {
            this->downloader[0].printAll();
        } else if (!strcmp(input.c_str(), "help")) {
            for (int i = 0; i < this->helpString.size(); i++) {
                cout << this->helpString[i];
            }
        }
        else {
            cout << "input not understood\n";
        }
    }
}

//private

void CLI::variableInit() {

    this->helpString = {"List of commands:\n\n",
                        "print                              Prints all packs loaded from the pack file together",
                        "with their bot, channel and server\n",
                        "print all                          Prints all servers, channels, bots and packs loaded from",
                        "the pack and server files\n",
                        "edit packs                         Opens the pack file in a text editor\n",
                        "edit servers                       Opens the sevrer file in a text editor\n",
                        "start                              Starts the download of all packs in the packfile\n\n",
                        "/msg bot xdcc send #pack           Downloads a single pack if the bot is contained",
                        "in the server file\n",
                        "add bot @ server/channel           Adds a bot to the server file\n",
                        "add /msg bot xdcc send #pack       Adds a pack to the pack file\n\n",
                        "help                               Prints a list of the available commands\n",
                        "quit                               Closes the program\n\n"};

}