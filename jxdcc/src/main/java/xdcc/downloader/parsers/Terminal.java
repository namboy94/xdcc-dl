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
import java.io.IOException;
import java.io.InputStreamReader;

/**
 * This class provides some simple methods for input/output from and to a terminal.
 *
 * Never modify this class, never upload it to Praktomat. This is only for your local use. If an assignment tells you to
 * use this class for input and output never use System.out or System.in in the same assignment.
 *
 * @author ITI, VeriAlg Group
 * @author IPD, SDQ Group
 * @version 4
 */
public final class Terminal {

    /**
     * BufferedReader for reading from standard input line-by-line.
     */
    private static BufferedReader in = new BufferedReader(new InputStreamReader(System.in));

    /**
     * Private constructor to avoid object generation.
     */
    private Terminal() {
    }

    /**
     * Print a String to the standard output.
     *
     * The String out must not be null.
     *
     * @param out
     *            The string to be printed.
     */
    public static void printLine(String out) {
        System.out.println(out);
    }

    /**
     * Reads a line from standard input.
     *
     * Returns null at the end of the standard input.
     *
     * Use Ctrl+D to indicate the end of the standard input.
     *
     * @return The next line from the standard input or null.
     */
    public static String readLine() {
        try {
            return in.readLine();
        } catch (IOException e) {
            /*
             * rethrow unchecked (!) exception to prevent students from being forced to use Exceptions before they have
             * been introduced in the lecture.
             */
            throw new RuntimeException(e);
        }
    }

}
