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

package xdcc.downloader;

import xdcc.downloader.bots.MainBot;
import xdcc.downloader.objects.Bot;
import xdcc.downloader.objects.Channel;
import xdcc.downloader.objects.Pack;
import xdcc.downloader.objects.Server;
import xdcc.downloader.parsers.*;

public class Main {

    public static void main(String[] args) {

        ConfigParser configParser = new ConfigParser(FileInputHelper.read(args[0]));
        String downloadLocation = configParser.getDownloadLocation();
        ServerParser serverParser = new ServerParser(FileInputHelper.read(args[1]));
        Server[] serverList = serverParser.getServerList();
        PackParser packParser = new PackParser(FileInputHelper.read(args[2]), serverList);
        
        for (int i = 0; i < serverList.length; i++) {
            Server server = serverList[i];
            for (int j = 0; j < server.getChannelList().length; j++) {
                Channel channel = server.getChannelList()[j];
                for (int k = 0; k < channel.getBotList().length; k++){
                    Bot bot = channel.getBotList()[k];
                    Pack[] botPacks = bot.getPackList();
                    MainBot mainBot = new MainBot(server.getName(), "#" + channel.getName(), 6667, "nambo", botPacks, downloadLocation);
                }
            }
        }
    }
}
