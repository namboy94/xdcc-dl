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
