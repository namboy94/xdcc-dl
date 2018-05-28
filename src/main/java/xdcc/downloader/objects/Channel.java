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

public class Channel {

    private String name;
    private Bot[] botList;

    public Channel(Server server, String name) {
        this.name = name;
        this.botList = new Bot[0];
    }

    public void addBot(Bot bot) {
        Bot[] newBotList = new Bot[this.botList.length + 1];
        for (int i = 0; i < this.botList.length; i++) {
            newBotList[i] = this.botList[i];
        }
        newBotList[this.botList.length] = bot;
        this.botList = newBotList;
    }

    public Bot[] getBotList() {
        return this.botList;
    }

    public String getName() {
        return this.name;
    }
}