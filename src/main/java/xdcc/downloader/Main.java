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
