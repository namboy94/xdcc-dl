/*
Copyright 2015-2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of jxdcc.

jxdcc is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

jxdcc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with jxdcc.  If not, see <http://www.gnu.org/licenses/>.
*/

package xdcc.downloader.parsers;

import xdcc.downloader.objects.Pack;
import xdcc.downloader.objects.Server;

public class PackParser {

    private Pack[] packList;
    private String[] inputFile;
    private Server[] serverList;

    public PackParser(String[] inputFile, Server[] serverList) {
        this.inputFile = inputFile;
        this.packList = new Pack[inputFile.length];
        this.serverList = serverList;
        parse();
    }

    private void parse() {
        for (int i = 0; i < this.inputFile.length; i++) {
            String noMsg = this.inputFile[i].split("/msg ")[1];
            String[] middleSplit = noMsg.split(" xdcc send ");
            Pack newPack = new Pack(middleSplit[0], "xdcc send " + middleSplit[1]);
            packList[i] = newPack;
            addToBot(newPack);
        }
    }

    private void addToBot(Pack pack) {
        boolean found = false;
        for (int i = 0; i < serverList.length && !found; i++) {
            for (int j = 0; j < serverList[i].getChannelList().length && !found; j++) {
                for (int k = 0; k < serverList[i].getChannelList()[j].getBotList().length && !found; k++) {
                    if (serverList[i].getChannelList()[j].getBotList()[k].getName().equals(pack.getPackArray()[0])) {
                        serverList[i].getChannelList()[j].getBotList()[k].addPack(pack);
                        found = true;
                    }
                }
            }
        }
        if (!found) {
            Terminal.printLine("Error, bot " + pack.getPackArray()[0] + "not found");
            System.exit(1);
        }
    }

    public Pack[] getPackList() {
        return this.packList;
    }

    public Server[] getServerList() {
        return this.serverList;
    }

    public String toString() {
        String out = "";
        out = out + "packList:\n\n";
        for (int i = 0; i < this.packList.length; i++) {
            out = out + "bot: " + this.packList[i].getPackArray()[0] + " msg: " + this.packList[i].getPackArray()[1] + "\n";
        }
        //out = out + "\nserverList:"
        return out;
    }
}
