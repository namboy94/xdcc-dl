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

import xdcc.downloader.objects.Bot;
import xdcc.downloader.objects.Channel;
import xdcc.downloader.objects.Server;

public class ServerParser {

    private Server[] serverList;
    private String[] serverFile;

    public ServerParser(String[] serverFile) {
        this.serverFile = serverFile;
        this.serverList = new Server[0];
        parse();
    }

    private void addServer(Server server) {
        Server[] newServerList = new Server[this.serverList.length + 1];
        for (int i = 0; i < this.serverList.length; i++) {
            newServerList[i] = this.serverList[i];
        }
        newServerList[this.serverList.length] = server;
        this.serverList = newServerList;
    }

    private int parseBot(int startLine, Channel channel) {
        if (startLine >= serverFile.length) {
            return startLine;
        }
        int i = startLine;
        int lastLine = i;
        String botName = this.serverFile[i].split("\\t\\tbot ")[1];
        Bot tempBot = new Bot(channel, botName);
        channel.addBot(tempBot);
        i++;

        if (i < this.serverFile.length) {
            if (this.serverFile[i].matches("\\t\\tbot\\s[^\\s]+")) {
                lastLine = parseBot(i, channel);
            }
        }
        return lastLine;
    }

    private int parseChannel(int startLine, Server server) {
        if (startLine >= serverFile.length) {
            return startLine;
        }
        int i = startLine;
        int lastLine = i;
        String channelName = this.serverFile[i].split("\\tchannel ")[1];
        Channel tempChannel = new Channel(server, channelName);
        server.addChannel(tempChannel);
        boolean incremented = false;
        i++;

        if (i < this.serverFile.length) {
            if (this.serverFile[i].matches("\\t\\tbot\\s[^\\s]+")) {
                i = parseBot(i, tempChannel);
                if (i < this.serverFile.length - 1) {
                    i++;
                    incremented = true;
                }
            }
            if (this.serverFile[i].matches("\\tchannel\\s[^\\s]+")) {
                lastLine = parseChannel(i, server);
            }
            else {
                if (incremented) {
                    return i - 1;
                }
                else {
                    return i;
                }
            }
        }
        return lastLine;
    }

    private int parseServer(int startLine, Server[] serverList) {
        if (startLine >= serverFile.length) {
            return startLine;
        }
        int i = startLine;
        int lastLine = i;
        String serverName = this.serverFile[i].split("server ")[1];
        Server tempServer = new Server(serverName);
        this.addServer(tempServer);
        boolean incremented = false;
        i++;

        if (i < this.serverFile.length) {
            if (this.serverFile[i].matches("\\tchannel\\s[^\\s]+")) {
                i = parseChannel(i, tempServer);
                if (i < this.serverFile.length - 1) {
                    i++;
                    incremented = true;
                }
            }
            if (this.serverFile[i].matches("server\\s[^\\s]+")) {
                lastLine = parseServer(i, serverList);
            }
            else {
                if (incremented) {
                    return i - 1;
                }
                else {
                    return i;
                }
            }
        }
        return lastLine;
    }

    private void parse() {
        for (int i = 0; i < serverFile.length; i++) {
            i = parseServer(i, this.serverList);
        }
    }

    public Server[] getServerList() {
        return this.serverList;
    }

    public String toString() {
        String out = "serverlist\n\n";
        for (int i = 0; i < this.serverList.length; i++) {
            out = out + this.serverList[i].getName() + "\n";
            for (int j = 0; j < this.serverList[i].getChannelList().length; j++) {
                out = out + "\t" + this.serverList[i].getChannelList()[j].getName() + "\n";
                for (int k = 0; k < this.serverList[i].getChannelList()[j].getBotList().length; k++) {
                    out = out + "\t\t" + this.serverList[i].getChannelList()[j].getBotList()[k].getName() + "\n";
                }
            }
        }
        return out;
    }

}
