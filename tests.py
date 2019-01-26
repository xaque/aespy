#!/usr/bin/env python3

import numpy as np
import aes


## Finite field arithmetic tests
assert(aes.ffAdd(0x57,0x83) == 0xd4)
assert(aes.xtime(0x57) == 0xae)
assert(aes.xtime(0xae) == 0x47)
assert(aes.xtime(0x47) == 0x8e)
assert(aes.xtime(0x8e) == 0x07)
assert(aes.ffMultiply(0x57,0x13) == 0xfe)
assert(aes.ffMultiply(0x13,0x57) == 0xfe)


## State transformation tests
state0 = np.zeros([4, 4], dtype=np.int8)
state0[0][0] = 0x19
state0[0][1] = 0xa0
state0[0][2] = 0x9a
state0[0][3] = 0xe9
state0[1][0] = 0x3d
state0[1][1] = 0xf4
state0[1][2] = 0xc6
state0[1][3] = 0xf8
state0[2][0] = 0xe3
state0[2][1] = 0xe2
state0[2][2] = 0x8d
state0[2][3] = 0x48
state0[3][0] = 0xbe
state0[3][1] = 0x2b
state0[3][2] = 0x2a
state0[3][3] = 0x08

state1 = np.zeros([4, 4], dtype=np.int8)
state1[0][0] = 0xd4
state1[0][1] = 0xe0
state1[0][2] = 0xb8
state1[0][3] = 0x1e
state1[1][0] = 0x27
state1[1][1] = 0xbf
state1[1][2] = 0xb4
state1[1][3] = 0x41
state1[2][0] = 0x11
state1[2][1] = 0x98
state1[2][2] = 0x5d
state1[2][3] = 0x52
state1[3][0] = 0xae
state1[3][1] = 0xf1
state1[3][2] = 0xe5
state1[3][3] = 0x30
aes.subBytes(state0)
assert((aes.subBytes(state0) == state1).all())


state2 = np.zeros([4, 4], dtype=np.int8)
state2[0][0] = 0xd4
state2[0][1] = 0xe0
state2[0][2] = 0xb8
state2[0][3] = 0x1e
state2[1][0] = 0xbf
state2[1][1] = 0xb4
state2[1][2] = 0x41
state2[1][3] = 0x27
state2[2][0] = 0x5d
state2[2][1] = 0x52
state2[2][2] = 0x11
state2[2][3] = 0x98
state2[3][0] = 0x30
state2[3][1] = 0xae
state2[3][2] = 0xf1
state2[3][3] = 0xe5
aes.shiftRows(state1)
assert((aes.shiftRows(state1) == state2).all())


state3 = np.zeros([4, 4], dtype=np.int8)
state3[0][0] = 0x04
state3[0][1] = 0xe0
state3[0][2] = 0x48
state3[0][3] = 0x28
state3[1][0] = 0x66
state3[1][1] = 0xcb
state3[1][2] = 0xf8
state3[1][3] = 0x06
state3[2][0] = 0x81
state3[2][1] = 0x19
state3[2][2] = 0xd3
state3[2][3] = 0x26
state3[3][0] = 0xe5
state3[3][1] = 0x9a
state3[3][2] = 0x7a
state3[3][3] = 0x4c
aes.mixColumns(state2)
assert((aes.mixColumns(state2) == state3).all())


state4 = np.zeros([4, 4], dtype=np.int8)
state4[0][0] = 0xa4
state4[0][1] = 0x68
state4[0][2] = 0x6b
state4[0][3] = 0x02
state4[1][0] = 0x9c
state4[1][1] = 0x9f
state4[1][2] = 0x5b
state4[1][3] = 0x6a
state4[2][0] = 0x7f
state4[2][1] = 0x35
state4[2][2] = 0xea
state4[2][3] = 0x50
state4[3][0] = 0xf2
state4[3][1] = 0x2b
state4[3][2] = 0x43
state4[3][3] = 0x49

key1 = np.zeros([4, 4], dtype=np.int8)
key1[0][0] = 0xa0
key1[0][1] = 0x88
key1[0][2] = 0x23
key1[0][3] = 0x2a
key1[1][0] = 0xfa
key1[1][1] = 0x54
key1[1][2] = 0xa3
key1[1][3] = 0x6c
key1[2][0] = 0xfe
key1[2][1] = 0x2c
key1[2][2] = 0x39
key1[2][3] = 0x76
key1[3][0] = 0x17
key1[3][1] = 0xb1
key1[3][2] = 0x39
key1[3][3] = 0x05
aes.addRoundKey(state3, key1)
assert((aes.addRoundKey(state3, key1) == state4).all())


## Key expansions tests

key0 = np.zeros([4, 4], dtype=np.int8)
key0[0][0] = 0x2b
key0[0][1] = 0x28
key0[0][2] = 0xab
key0[0][3] = 0x09
key0[1][0] = 0x7e
key0[1][1] = 0xae
key0[1][2] = 0xf7
key0[1][3] = 0xcf
key0[2][0] = 0x15
key0[2][1] = 0xd2
key0[2][2] = 0x15
key0[2][3] = 0x4f
key0[3][0] = 0x16
key0[3][1] = 0xa6
key0[3][2] = 0x88
key0[3][3] = 0x3c
aes.nextRoundKey(key0, 1)
assert((aes.nextRoundKey(key0, 1) == key1).all())

key2 = np.zeros([4, 4], dtype=np.int8)
key2[0][0] = 0xf2
key2[0][1] = 0x7a
key2[0][2] = 0x59
key2[0][3] = 0x73
key2[1][0] = 0xc2
key2[1][1] = 0x96
key2[1][2] = 0x35
key2[1][3] = 0x59
key2[2][0] = 0x95
key2[2][1] = 0xb9
key2[2][2] = 0x80
key2[2][3] = 0xf6
key2[3][0] = 0xf2
key2[3][1] = 0x43
key2[3][2] = 0x7a
key2[3][3] = 0x7f
aes.nextRoundKey(key1, 2)
assert((aes.nextRoundKey(key1, 2) == key2).all())


## Cipher tests

state = np.array([[0x19,0xa0,0x9a,0xe9],
                  [0x3d,0xf4,0xc6,0xf8],
                  [0xe3,0xe2,0x8d,0x48],
                  [0xbe,0x2b,0x2a,0x08]], dtype=np.int8)

sub = np.array([[0xd4,0xe0,0xb8,0x1e],
                [0x27,0xbf,0xb4,0x41],
                [0x11,0x98,0x5d,0x52],
                [0xae,0xf1,0xe5,0x30]], dtype=np.int8)

shift = np.array([[0xd4, 0xe0, 0xb8, 0x1e],
                  [0xbf, 0xb4, 0x41, 0x27],
                  [0x5d, 0x52, 0x11, 0x98],
                  [0x30, 0xae, 0xf1, 0xe5]], dtype=np.int8)

mix = np.array([[0x04, 0xe0, 0x48, 0x28],
                [0x66, 0xcb, 0xf8, 0x06],
                [0x81, 0x19, 0xd3, 0x26],
                [0xe5, 0x9a, 0x7a, 0x4c]], dtype=np.int8)

rounds = np.array([[0xa4, 0x68, 0x6b, 0x02],
                   [0x9c, 0x9f, 0x5b, 0x6a],
                   [0x7f, 0x35, 0xea, 0x50],
                   [0xf2, 0x2b, 0x43, 0x49]], dtype=np.int8)

key = np.array([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
				0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c], dtype=np.int8)
key = key.transpose()

assert((aes.subBytes(state) == sub).all())
assert((aes.shiftRows(sub) == shift).all())
assert((aes.mixColumns(shift) == mix).all())
keystate = np.zeros([4, 4], dtype=np.int8)
for i in range(4):
    for j in range(4):
        keystate[i][j] = key[i*4 + j]
keystate = keystate.transpose()
assert((aes.addRoundKey(mix, aes.nextRoundKey(keystate, 1)) == rounds).all())



in1 = np.array([0x32, 0x43, 0xf6, 0xa8,
				0x88, 0x5a, 0x30, 0x8d,
				0x31, 0x31, 0x98, 0xa2,
				0xe0, 0x37, 0x07, 0x34], dtype=np.int8)

result = np.array([0x39, 0x25, 0x84, 0x1d,
				   0x02, 0xdc, 0x09, 0xfb,
				   0xdc, 0x11, 0x85, 0x97,
				   0x19, 0x6a, 0x0b, 0x32], dtype=np.int8)

output = aes.cipher(in1, key)
assert((output == result).all())
