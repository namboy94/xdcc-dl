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