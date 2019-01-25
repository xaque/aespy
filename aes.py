#!/usr/bin/env python3
import numpy as np

def mixColumns(state):
    result = np.zeros([4, 4], dtype=np.int8)
    for i, col in enumerate(state.transpose()):
        newcol = np.zeros(4, dtype=np.int8)
        newcol[0] = ffMultiply(0x02, col[0]) ^ ffMultiply(0x03, col[1]) ^ col[2] ^ col[3]
        newcol[1] = col[0] ^ ffMultiply(0x02, col[1]) ^ ffMultiply(0x03, col[2]) ^ col[3]
        newcol[2] = col[0] ^ col[1] ^ ffMultiply(0x02, col[2]) ^ ffMultiply(0x03, col[3])
        newcol[3] = ffMultiply(0x03, col[0]) ^ col[1] ^ col[2] ^ ffMultiply(0x02, col[3])
        result[i] = newcol
    return result.transpose()

def stateAdd(col1, col2, col3 = np.zeros(4, dtype=np.int8), col4 = np.zeros(4, dtype=np.int8)):
    for i in range(0, len(col1)):
        col1[i] ^= col2[i]
        col1[i] ^= col3[i]
        col1[i] ^= col4[i]
    return col1

def ffAdd(b1, b2):
    return b1 ^ b2

def ffMultiply(b1, b2):
    num = b1
    xt = b1
    mask = 0x02
    for i in range(0, 7):
        xt = xtime(xt)
        if b2 & mask:
            num ^= xt
        mask <<= 1
    return num

def xtime(num):
    num <<= 1
    if num & 0x100:
        num ^= 0x11b
    return num

state = np.zeros([4, 4], dtype=np.int8)
state[0][0] = 0x00
state[0][1] = 0x01
state[0][2] = 0x02
state[0][3] = 0x03
state[1][0] = 0x04
state[1][1] = 0x05
state[1][2] = 0x06
state[1][3] = 0x07
state[2][0] = 0x08
state[2][1] = 0x09
state[2][2] = 0x0a
state[2][3] = 0x0b
state[3][0] = 0x0c
state[3][1] = 0x0d
state[3][2] = 0x0e
state[3][3] = 0x0f
print(state)
print()
state = mixColumns(state)
print(state)
print()
state = mixColumns(state)
print(state)
print()
state = mixColumns(state)
print(state)
print()
state = mixColumns(state)
print(state)
print()
state = mixColumns(state)
print(state)
print()