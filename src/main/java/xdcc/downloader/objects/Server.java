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