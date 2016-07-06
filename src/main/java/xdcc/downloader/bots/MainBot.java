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
