/*
Copyright 2015-2017 Hermann Krumrey <hermann@krumreyh.com>

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
 *
 * XDCC-Download is a program which automatically downloads a list of XDCC packs via IRC.
 * It allows the user to input the list as direct commands or for more advanced usage via a
 * input file providing the information for the packs to be downloaded
 */

#ifdef _WIN32
#include <windows>
#endif

#include <iostream>
#include "Objects/Config.h"
#include "Objects/ServerList.h"
#include "Downloaders/HexChatPythonDownloader.h"
#include "Interface/CLI.h"

/**
 * The Main Function that runs the program
 */
int main() {

    //TODO: GUI/CLI choice

#ifdef __linux__
    Config config("/home/" + string(getenv("USER")) + "/.xdcc-download/files/config");
#elif _WIN32
    //TODO: Windows Implementation
#endif

    ServerList serverList(config);
    HexChatPythonDownloader downloader(config, serverList);
    CLI cli(downloader, config);
    cli.mainLoop();

    return 0;
}