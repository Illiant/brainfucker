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


class Brainfucker(object):
    STATE_NORMAL = 0
    STATE_EOP = 1  # End of program

    _size = 512
    _memory = []
    _program = []
    _jumptable = {}

    _sp = 0  # Storage pointer
    _ip = 0  # Instruction pointer
    _clock = 0

    _state = 0  # Natural state

    _input = []
    _output = []

    def __init__(self, memory=512):
        self._size = memory
        self.reset()

    def step(self):
        """
        Steps through program
        Returns the command executed
        """
        self._clock += 1

        if self._program is None:
            return None

        if self._state == self.STATE_EOP:
            return None

        if self._ip >= len(self._program):
            return None

        cmd = self._program[self._ip]

        if cmd == '>':
            self._sp += 1

        elif cmd == '<':
            self._sp -= 1

        elif cmd == '+':
            self._memory[self._sp] = (self._memory[self._sp] + 1) % 256

        elif cmd == '-':
            if self._memory[self._sp] > 0:
                self._memory[self._sp] -= 1
            else:
                self._memory[self._sp] = 255

        elif cmd == '.':
            self._output.append(self._memory[self._sp])

        elif cmd == ',':
            assert len(self._input) > 0
            self._memory[self._sp] = self._input.pop()

        elif cmd == '[':
            if self._memory[self._sp] == 0:
                self._ip = self._jumptable[self._ip]
                return

        elif cmd == ']':
            if self._memory[self._sp] != 0:
                self._ip = self._jumptable[self._ip]
                return

        self._ip += 1

        if self._ip > len(self._program):
            # Program stopped
            self._state = self.STATE_EOP

        return cmd

    def reset(self):
        """
        Resets the machine
        """
        self._sp = 0
        self._clock = 0
        self._ip = 0
        self._memory = [0 for i in range(self._size)]

    def program(self, program):
        self._program = list(program)
        self.compile()

    def compile(self):
        """
        Build a jumptable
        """
        start = []
        for ip in range(len(self._program)):
            i = self._program[ip]
            if i == '[':
                start.append(ip)
            elif i == ']':
                b = start.pop()
                self._jumptable[ip] = b
                self._jumptable[b] = ip

    def get_output_length(self):
        """
            Returns the number of bytes available at output
        """
        return len(self._output)

    def get_output(self, n=None, clear=True):
        """
        Returns the output
        if b is an integer, only the n first bytes

        clears the output
        """

        n = n or self.get_output_length()
        assert(n >= 0)
        assert(n <= len(self._output))

        out = self._output[:n]

        if clear:
            self._output = self._output[n:]

        return out

    def input(self, i):
        assert isinstance(i, int)
        assert i >= 0
        assert i < 256
        self._input.append(i)
