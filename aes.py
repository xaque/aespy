#!/usr/bin/env python3
import numpy as np
import copy



### AES given definitions ###

# Rcon[] is 1-based, so the first entry is just a place holder 
Rcon = [ 0x00000000, 
           0x01000000, 0x02000000, 0x04000000, 0x08000000, 
           0x10000000, 0x20000000, 0x40000000, 0x80000000, 
           0x1B000000, 0x36000000, 0x6C000000, 0xD8000000, 
           0xAB000000, 0x4D000000, 0x9A000000, 0x2F000000, 
           0x5E000000, 0xBC000000, 0x63000000, 0xC6000000, 
           0x97000000, 0x35000000, 0x6A000000, 0xD4000000, 
           0xB3000000, 0x7D000000, 0xFA000000, 0xEF000000, 
           0xC5000000, 0x91000000, 0x39000000, 0x72000000, 
           0xE4000000, 0xD3000000, 0xBD000000, 0x61000000, 
           0xC2000000, 0x9F000000, 0x25000000, 0x4A000000, 
           0x94000000, 0x33000000, 0x66000000, 0xCC000000, 
           0x83000000, 0x1D000000, 0x3A000000, 0x74000000, 
           0xE8000000, 0xCB000000, 0x8D000000]

Sbox = [
    [ 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76 ] ,
    [ 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0 ] ,
    [ 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15 ] ,
    [ 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75 ] ,
    [ 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84 ] ,
    [ 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf ] ,
    [ 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8 ] ,
    [ 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2 ] ,
    [ 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73 ] ,
    [ 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb ] ,
    [ 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79 ] ,
    [ 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08 ] ,
    [ 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a ] ,
    [ 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e ] ,
    [ 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf ] ,
    [ 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 ]
    ]

InvSbox = [
    [ 0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb ] ,
    [ 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb ] ,
    [ 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e ] ,
    [ 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25 ] ,
    [ 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92 ] ,
    [ 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84 ] ,
    [ 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06 ] ,
    [ 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b ] ,
    [ 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73 ] ,
    [ 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e ] ,
    [ 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b ] ,
    [ 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4 ] ,
    [ 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f ] ,
    [ 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef ] ,
    [ 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61 ] ,
    [ 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d ]
    ]



### Finite field arithmetic ###

def ffAdd(b1, b2):
    return b1 ^ b2

def ffMultiply(b1, b2):
    num = 0
    xt = b1
    mask = 0x01
    for i in range(0, 8):
        if b2 & mask:
            num ^= xt
        mask <<= 1
        xt = xtime(xt)
    return num

def xtime(num):
    num <<= 1
    if num & 0x100:
        num ^= 0x11b
    return num



### Key expansion ###

def expandKey(key):
    np.set_printoptions(formatter={'int':hex})
    #print(key)
    expanded = []
    # Convert key byte array into array of words
    currentWord = np.int32(0)
    for i in range(len(key)):
        currentWord ^= (key[i] & 0x000000ff)
        #print(hex(currentWord))
        if (i % 4) == 3:
            #print("word: ", hex(currentWord))
            expanded.append(currentWord)
            currentWord = np.int32(0)
        currentWord <<= 8
    
    #
    #print(expanded)
    #print([hex(no) for no in expanded])
    divider = int(len(key) / 4)
    rounds = int(7 + (len(key) / 4))
    expandedSize = rounds * 4
    expandedI = len(expanded)
    for i in range(expandedI, expandedSize):
        nextWord = np.int32(0)
        if (i % divider == 0):
            #print(i)
            # First column of round key
            nextWord = expanded[i - 1]
            #print(hex(nextWord))
            nextWord = rrotWord(nextWord)
            #print(hex(nextWord))
            nextWord = ssubWord(nextWord)
            #print(hex(nextWord))
            nextWord ^= expanded[i - divider] ^ Rcon[int(i / divider)]#TODO not sure if this is right for larger keys
            #print(hex(nextWord))
            #print()
        else:
            # Other columns
            nextWord = expanded[i - 1]
            if divider == 8 and (i-4) % divider == 0:
                nextWord = ssubWord(nextWord)
            nextWord ^= expanded[i - divider]
        expanded.append(nextWord)
    #print(len(expanded))
    #print([hex(no) for no in expanded])
    #for i in range(len(expanded)):
    #    if i % 4 == 0:
    #        print()
    #    print(hex(expanded[i]), "\t", end='')
    #print()
    return expanded

def rrotWord(word):
    tmp = word & 0xff000000
    tmp >>= 24
    tmp &= 0xff
    newWord = word << 8
    newWord &= 0xffffff00
    return newWord | tmp

def ssubWord(word):
    b1 = (0xff000000 & word) >> 24
    b2 = (0x00ff0000 & word) >> 16
    b3 = (0x0000ff00 & word) >> 8
    b4 = 0x000000ff & word
    b1 = subByte(b1)
    b2 = subByte(b2)
    b3 = subByte(b3)
    b4 = subByte(b4)
    b1 <<= 24
    b2 <<= 16
    b3 <<= 8
    #just in case
    #b1 &= 0xff000000
    #b2 &= 0x00ff0000
    #b3 &= 0x0000ff00
    #b4 &= 0x000000ff
    return b1 | b2 | b3 | b4

def nextRoundKey(key, roundi=1):
    keyCopy = key.copy().transpose()
    nextKey = np.zeros([4, 4], dtype=np.int8)
    col0 = keyCopy[3]
    col0 = rotWord(col0)
    col0 = subWord(col0)
    col0 = colAdd(col0, keyCopy[0])
    rcon = Rcon[roundi]
    rcon = (rcon >> 24) & 0xff
    col0[0] ^= rcon
    nextKey[0] = col0
    col1 = colAdd(col0, keyCopy[1])
    nextKey[1] = col1
    col2 = colAdd(col1, keyCopy[2])
    nextKey[2] = col2
    keyCopy = key.transpose()
    col3 = colAdd(col2, keyCopy[3])
    nextKey[3] = col3
    return nextKey.transpose()

def rotWord(word):
    tmp = word[0]
    for j in range(len(word)-1):
        word[j] = word[j+1]
    word[len(word)-1] = tmp
    return word

def subWord(word):
    for i in range(len(word)):
        word[i] = subByte(word[i])
    return word



### State transformations ###

def addRoundKey(state, key):
    result = state.copy()
    for i in range(4):
        for j in range(4):
            result[i][j] ^= key[i][j]
    return result

def subBytes(state):
    result = state.copy()
    for i in range(4):
        for j in range(4):
            result[i][j] = subByte(result[i][j])
    return result

def shiftRows(state):
    result = state.copy()
    for i in range(4):
        result[i] = rotateRow(result[i], i)
    return result

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

def invSubBytes(state):
    result = state.copy()
    for i in range(4):
        for j in range(4):
            result[i][j] = subByte(result[i][j], sbox=InvSbox)
    return result

def invShiftRows(state):
    result = state.copy()
    result[1] = rotateRow(result[1], 3)
    result[2] = rotateRow(result[2], 2)
    result[3] = rotateRow(result[3], 1)
    return result

def invMixColumns(state):
    result = np.zeros([4, 4], dtype=np.int8)
    for i, col in enumerate(state.transpose()):
        newcol = np.zeros(4, dtype=np.int8)
        newcol[0] = ffMultiply(0x0e, col[0]) ^ ffMultiply(0x0b, col[1]) ^ ffMultiply(0x0d, col[2]) ^ ffMultiply(0x09, col[3])
        newcol[1] = ffMultiply(0x09, col[0]) ^ ffMultiply(0x0e, col[1]) ^ ffMultiply(0x0b, col[2]) ^ ffMultiply(0x0d, col[3])
        newcol[2] = ffMultiply(0x0d, col[0]) ^ ffMultiply(0x09, col[1]) ^ ffMultiply(0x0e, col[2]) ^ ffMultiply(0x0b, col[3])
        newcol[3] = ffMultiply(0x0b, col[0]) ^ ffMultiply(0x0d, col[1]) ^ ffMultiply(0x09, col[2]) ^ ffMultiply(0x0e, col[3])
        result[i] = newcol
    return result.transpose()



### Helper functions ###

def subByte(byte, sbox=Sbox):
    left = (byte >> 4) & 0x0f
    right = byte & 0x0f
    return sbox[left][right]

def rotateRow(row, n):
    for i in range(n):
        row = rotWord(row)
    return row

def colAdd(col1, col2):
    for i in range(0, len(col1)):
        col1[i] ^= col2[i]
    return col1

def getRoundKey(expandedKey, n):
    key = np.zeros([4, 4], dtype=np.int8)
    for i in range(4):
        word = expandedKey[(n * 4) + i]
        #print(hex(word))
        for j in range(4):
            byte = word << (j*8)
            mask = 0xff000000
            byte &= mask
            byte >>= 24
            byte &= 0xff
            key[j][i] = byte
            #print(hex(byte))
    return key



### Cipher ###

def cipher(inp, k):
    # 1d to 2d
    state = np.zeros([4, 4], dtype=np.int8)
    for i in range(4):
        for j in range(4):
            state[i][j] = inp[i*4 + j]
    state = state.transpose()
    
    expandedKey = expandKey(k)
    numMainRounds = int(len(expandedKey) / 4) - 2
    roundNum = 0

    # Initial round
    state = addRoundKey(state, getRoundKey(expandedKey, roundNum))
    roundNum += 1

    # Main rounds
    for _ in range(numMainRounds):
        state = subBytes(state)
        state = shiftRows(state)
        state = mixColumns(state)
        state = addRoundKey(state, getRoundKey(expandedKey, roundNum))
        roundNum += 1

    # Final round
    state = subBytes(state)
    state = shiftRows(state)
    state = addRoundKey(state, getRoundKey(expandedKey, roundNum))
    roundNum += 1
    print(roundNum)

    # Final state to 1d array
    state = state.transpose()
    output = np.zeros(16, dtype=np.int8)
    for i in range(4):
        for j in range(4):
            output[i*4 + j] = state[i][j]
    return output

def invCipher(inp, k):
    # 1d to 2d
    state = np.zeros([4, 4], dtype=np.int8)
    for i in range(4):
        for j in range(4):
            state[i][j] = inp[i*4 + j]
    state = state.transpose()

    expandedKey = expandKey(k)
    numMainRounds = int(len(expandedKey) / 4) - 2
    roundNum = numMainRounds + 1

    # Initial round
    state = addRoundKey(state, getRoundKey(expandedKey, roundNum))
    roundNum -= 1

    # Main rounds
    for _ in range(numMainRounds):
        state = invShiftRows(state)
        state = invSubBytes(state)
        state = addRoundKey(state, getRoundKey(expandedKey, roundNum))
        roundNum -= 1
        state = invMixColumns(state)

    # Final round
    state = invShiftRows(state)
    state = invSubBytes(state)
    state = addRoundKey(state, getRoundKey(expandedKey, roundNum))

    # Final state to 1d array
    state = state.transpose()
    output = np.zeros(16, dtype=np.int8)
    for i in range(4):
        for j in range(4):
            output[i*4 + j] = state[i][j]
    return output