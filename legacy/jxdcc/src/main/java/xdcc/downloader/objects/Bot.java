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
