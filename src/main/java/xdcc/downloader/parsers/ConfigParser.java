package xdcc.downloader.parsers;

public class ConfigParser {

    private String[] configFile;
    private String downloadLocation;

    public ConfigParser(String[] configFile) {
        this.configFile = configFile;
        this.parse();
    }

    private void parse () {
        for (int i = 0; i < this.configFile.length; i++) {
            if (this.configFile[i].toLowerCase().contains("download location: ")) {
                this.downloadLocation = this.configFile[i].split("download location: ")[1];
            }
        }
    }

    public String getDownloadLocation() {
        return this.downloadLocation;
    }

    public String toString() {
        String out = "";
        out = out + this.downloadLocation + "\n";
        return out;
    }
}
