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

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

/**
 * Helper class for reading text files.
 *
 * @author IPD Reussner, KIT
 * @author ITI Sinz, KIT
 * @version 1.1
 */
public final class FileInputHelper {

    /**
     * Private constructor to avoid instantiation.
     */
    private FileInputHelper() {
        // intentionally left blank
    }

    /**
     * Reads the specified file and returns its content as a String array, where the first array field contains the
     * file's first line, the second field contains the second line, and so on.
     *
     * @param file
     *            the file to be read
     * @return the content of the file
     */
    public static String[] read(String file) {
        StringBuilder result = new StringBuilder();

        FileReader in = null;
        try {
            in = new FileReader(file);
        } catch (FileNotFoundException e) {
            Terminal.printLine("Error, " + e.getMessage());
            System.exit(1);
        }

        BufferedReader reader = new BufferedReader(in);
        try {
            String line = reader.readLine();
            while (line != null) {
                result.append(line);
                line = reader.readLine();
                if (line != null) {
                    result.append("\n");
                }
            }
        } catch (IOException e) {
            Terminal.printLine("Error, " + e.getMessage());
            System.exit(1);
        } finally {
            try {
                reader.close();
            } catch (IOException e) {
                // no need for handling this exception
            }
        }

        return result.toString().split("\n");
    }

}
