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

package xdcc.downloader.bots;

import xdcc.downloader.bots.listeners.MainListener;
import org.pircbotx.Configuration;
import org.pircbotx.PircBotX;
import org.pircbotx.exception.IrcException;
import xdcc.downloader.objects.Pack;

import java.io.IOException;

public class MainBot {

    public PircBotX bot;

    public MainBot(String server, String channel, int port, String nick, Pack[] botPacks, String downloadLocation) {

        Configuration config = new Configuration.Builder()
                .setName(nick)
                .addServer(server, port)
                .addAutoJoinChannel(channel)
                .addListener(new MainListener(nick, botPacks, downloadLocation))
                .buildConfiguration();

        this.bot = new PircBotX(config);

        try {
            this.bot.startBot();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (IrcException e) {
            e.printStackTrace();
        }
    }

    public PircBotX getBot() {
        return this.bot;
    }
}
