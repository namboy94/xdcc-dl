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

package xdcc.downloader.objects;

import xdcc.downloader.parsers.Terminal;

public class Server {

    private String name;
    private Channel[] channelList;

    public Server(String name) {
        this.name = name;
        this.channelList = new Channel[0];
    }

    public void addChannel(Channel channel) {
        Channel[] newChannelList = new Channel[this.channelList.length + 1];
        for (int i = 0; i < this.channelList.length; i++) {
            newChannelList[i] = this.channelList[i];
        }
        newChannelList[this.channelList.length] = channel;
        this.channelList = newChannelList;
    }

    public Bot searchBot(String botName) {
        for (int i = 0; i < channelList.length; i++) {
            for (int j = 0; j < channelList[i].getBotList().length; j++) {
                if (channelList[i].getBotList()[j].getName().equals(botName)) {
                    return channelList[i].getBotList()[j];
                }
            }
        }
        Terminal.printLine("Error, bot " + botName + " not found");
        System.exit(1);
        return null;
    }

    public Channel[] getChannelList() {
        return this.channelList;
    }

    public String getName() {
        return this.name;
    }
}