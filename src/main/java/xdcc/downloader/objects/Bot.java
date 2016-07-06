package xdcc.downloader.objects;

public class Bot {

    private String name;
    Pack[] packList;

    public Bot(Channel channel, String name) {
        this.name = name;
        this.packList = new Pack[0];
    }

    public String getName() {
        return this.name;
    }

    public void addPack(Pack pack) {
        Pack[] newPackList = new Pack[this.packList.length + 1];
        for (int i = 0; i < this.packList.length; i++) {
            newPackList[i] = this.packList[i];
        }
        newPackList[this.packList.length] = pack;
        this.packList = newPackList;
    }

    public Pack[] getPackList() {
        return packList;
    }
}
