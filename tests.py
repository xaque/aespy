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