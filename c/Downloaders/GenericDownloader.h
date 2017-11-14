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

#ifndef XDCC_DOWNLOAD_GENERICDOWNLOADER_H
#define XDCC_DOWNLOAD_GENERICDOWNLOADER_H

#include "../Objects/ServerList.h"

/**
 * Abstract class that defines the interface of a Downloader
 */
class GenericDownloader {

public:

    //Functional functions
    virtual void downloadAll() = 0;
    virtual void addSinglePack(string addPackString) = 0;
    virtual void addSingleBot(string addBotString) = 0;
    virtual void downloadSinglePack(string packString) = 0;
    virtual void editPacks() = 0;
    virtual void editServers() = 0;
    virtual void printAll() = 0;
    virtual void printPacks() = 0;

};

#endif //XDCC_DOWNLOAD_GENERICDOWNLOADER_H
