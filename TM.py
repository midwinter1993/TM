#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class TM(object):
    def __init__(self, *arg):
        super(TM, self).__init__()
        self.state_, self.pos_ = (1, 1)
        self.tape_ = [0]
        for num in arg:
            self.tape_.extend([1 for i in xrange(num + 1)])
            self.tape_.append(0)

    def curr_tape_bit(self):
        return self.tape_[self.pos_]

    def exec_inst(self, inst):
        assert type(inst) is str and len(inst) >= 3

        match = re.match(r'([01])([LROlro])(\d+)', inst.strip())
        assert match.groups()

        act, move, state = match.groups()
        self.tape_[self.pos_] = 0 if act == '0' else 1

        step = {'R': 1, 'L': -1, 'O': 0}
        self.pos_ += step[move.upper()]

        if self.pos_ >= len(self.tape_):
            self.tape_.append(0)
        if self.pos_ < 0:
            self.tape_.insert(0, 0)
            self.pos_ = 0

        self.state_ = int(state)

    def exec_table(self, table):
        max_state = len(table)
        while 0 <= self.state_ <= max_state:
            inst = table[self.state_ - 1][self.curr_tape_bit()]
            if inst == '':
                return
            self.exec_inst(inst)

    def bit_tape_str(self):
        return ''.join(map(str, self.tape_))

    def number_tape_str(self):
        sticks = re.findall(r'01+', self.bit_tape_str())
        return ','.join([str(len(i) - 2) for i in sticks])

    def state_pos_str(self):
        return '(%d: %d) ' % (self.state_, self.pos_)

    def print_number_tape(self):
        print self.state_pos_str() + self.number_tape_str()

    def __str__(self):
        self.print_number_tape()
        return self.state_pos_str() + self.bit_tape_str()


if __name__ == "__main__":
    t = TM(4)
    print t
    table = [
        ('0R6', '0R2'),
        ('0R3', '1R2'),
        ('1L4', '1R3'),
        ('0L5', '1L4'),
        ('1R1', '1L5'),
        ('0R7', '1L6'),
    ]
    t.exec_table(table)
    print t
