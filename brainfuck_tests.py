#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
    Brainfuck implementation
    Copyright (C) 2015  Greger Stolt Nilsen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division


import unittest

import brainfuck


class TestTests(unittest.TestCase):
    def test_failing(self):
        self.assertFalse(False)

    def test_passing(self):
        self.assertTrue(True)


class TestInitial(unittest.TestCase):
    def setUp(self):
        self.bf = brainfuck.Brainfucker(1024)

    def test_blank(self):
        self.assertEqual(self.bf._clock, 0)
        self.assertEqual(self.bf._sp, 0)

        self.assertEqual(len(self.bf._memory), 1024)
        self.assertEqual(self.bf.get_output_length(), 0)

    def test_step(self):
        self.assertEqual(self.bf._clock, 0)
        self.assertEqual(self.bf._sp, 0)

        self.bf.step()

        self.assertEqual(self.bf._clock, 1)

    def test_reset(self):
        self.assertEqual(self.bf._clock, 0)
        self.assertEqual(self.bf._sp, 0)
        self.assertIsNone(self.bf.step())
        self.assertEqual(self.bf._clock, 1)
        self.bf.reset()
        self.assertEqual(self.bf._clock, 0)
        self.assertEqual(self.bf._sp, 0)

    def test_program(self):
        self.bf.program('><')
        self.assertEqual(self.bf._clock, 0)
        self.bf.step()

        self.assertEqual(self.bf._clock, 1)
        self.assertEqual(self.bf._sp, 1)

        self.bf.step()

        self.assertEqual(self.bf._clock, 2)
        self.assertEqual(self.bf._sp, 0)

    def test_data_manipulation(self):
        self.assertEqual(self.bf._memory[0], 0)

        self.bf.program('+')

        self.bf.step()

        self.assertEqual(self.bf._sp, 0)
        self.assertEqual(self.bf._memory[0], 1)

        self.bf.reset()
        self.bf.program('-')

        self.bf.step()

        self.assertEqual(self.bf._sp, 0)
        self.assertEqual(self.bf._memory[0], 255)

    def test_output(self):
        self.assertEqual(self.bf.get_output_length(), 0)

        self.bf.program('.')

        self.bf.step()
        self.assertEqual(self.bf.get_output_length(), 1)

        output = self.bf.get_output()

        self.assertEqual(len(output), 1)

        self.assertEqual(output[0], 0)

        self.assertEqual(self.bf.get_output_length(), 0)

    def test_input(self):
        self.bf.program(',')
        self.bf.input(25)

        self.bf.step()
        self.assertEqual(self.bf._memory[0], 25)

    def test_jump(self):
        self.bf.program('[+]')
        self.bf.step()

        self.assertEqual(self.bf._ip, 2)
