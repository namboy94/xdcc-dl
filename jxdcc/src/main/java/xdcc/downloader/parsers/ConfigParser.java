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
