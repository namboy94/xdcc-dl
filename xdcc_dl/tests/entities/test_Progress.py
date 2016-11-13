"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of xdcc_dl.

    xdcc_dl is a program that allows downloading files via the XDCC
    protocol via file serving bots on IRC networks.

    xdcc_dl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    xdcc_dl is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with xdcc_dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import time
import unittest
from xdcc_dl.entities.Progress import Progress


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.progress = Progress(10)
        self.callback_called = False

    def tearDown(self):
        pass

    def test_single_progress(self):

        self.progress.set_single_progress(100)
        self.progress.set_single_progress_total(1000)
        self.assertEqual(self.progress.get_single_progress(), 100)
        self.assertEqual(self.progress.get_single_progress_total(), 1000)
        self.assertEqual(self.progress.get_single_progress_percentage(), 10.0)

        self.progress.add_single_progress(100)
        self.assertEqual(self.progress.get_single_progress(), 200)
        self.assertEqual(self.progress.get_single_progress_percentage(), 20.0)

        self.assertLess(self.progress.get_total_percentage(), 10.0)
        self.assertLess(0.0, self.progress.get_total_percentage())

    def test_next_file(self):

        self.assertEqual(self.progress.get_total_percentage(), 0.0)
        self.progress.next_file()
        self.assertEqual(self.progress.get_total_percentage(), 10.0)

    def test_callback_handler(self):

        def callback_tester(single_progress, single_total, single_progress_percentage,
                            total_progress, total_total, total_percentage, current_speed, average_speed):

            self.callback_called = True
            self.assertEqual(single_progress, 300)
            self.assertEqual(single_total, 1000)
            self.assertEqual(single_progress_percentage, 30.0)
            self.assertEqual(total_progress, 0)
            self.assertEqual(total_total, 2)
            self.assertLess(total_percentage, 50.0)
            self.assertLess(0.0, total_percentage)
            self.assertAlmostEqual(current_speed, 100, delta=5)
            self.assertAlmostEqual(average_speed, 100, delta=5)

        progress_with_callback = Progress(2, callback=callback_tester)
        progress_with_callback.set_single_progress_total(1000)
        time.sleep(3)
        progress_with_callback.add_single_progress(300)

        self.assertTrue(self.callback_called)

    def test_current_download_speed(self):

        self.assertEqual(self.progress.calculate_current_download_speed(), 0)
        self.progress.add_single_progress(50)
        time.sleep(0.25)

        self.assertEqual(self.progress.calculate_current_download_speed(), 0)
        self.progress.add_single_progress(50)
        time.sleep(0.75)

        self.assertAlmostEqual(self.progress.calculate_current_download_speed(), 100, delta=5)

    def test_for_zero_division_errors(self):

        progress = Progress(0)
        self.assertEqual(progress.get_single_progress_percentage(), 0.0)
        self.assertEqual(progress.get_total_percentage(), 0.0)

    def test_finished_numbers(self):

        while self.progress.get_total_percentage() < 100.0:
            self.progress.set_single_progress_total(100)
            while self.progress.get_single_progress_percentage() < 100.0:
                self.progress.add_single_progress(1)
            self.progress.next_file()

        self.assertEqual(self.progress.get_total_percentage(), 100.0)
        self.assertEqual(self.progress.get_single_progress_percentage(), 100.0)
        self.assertEqual(self.progress.get_single_progress(), 100)
        self.assertEqual(self.progress.get_single_progress(), self.progress.get_single_progress_total())

    def test_going_past_total_limit(self):

        while self.progress.get_total_percentage() < 100.0:
            self.progress.next_file()

        self.assertEqual(self.progress.get_total_percentage(), 100.0)
        self.assertEqual(self.progress.total_progress, 10)
        self.progress.next_file()
        self.assertEqual(self.progress.get_total_percentage(), 100.0)
        self.assertEqual(self.progress.total_progress, 10)
        self.progress.next_file()
        self.assertEqual(self.progress.get_total_percentage(), 100.0)
        self.assertEqual(self.progress.total_progress, 10)
