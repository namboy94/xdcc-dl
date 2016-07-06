package xdcc.downloader.objects;

public class Pack {

    private String[] pack;

    public Pack(String target, String pack) {
        this.pack = new String[2];
        this.pack[0] = target;
        this.pack[1] = pack;
    }

    public String[] getPackArray() {
        return this.pack;
    }
}
