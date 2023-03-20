## @Autor: Manzanares Peña Jorge Luis
## @Fecha: 17 de marzo de 2023
## @Decripción: Implementación Simplified DES

import fileinput

# s-box s0
S0 = [['01','00','11','10'],
      ['11','10','01','00'],
      ['00','10','01','11'],
      ['11','01','11','10']]

# s-box s1
S1 = [['00','01','10','11'],
      ['10','00','01','11'],
      ['11','00','01','00'],
      ['10','01','00','11']]

initial_p = [1,5,2,0,3,7,4,6]       # initial permutation
inverse_p = [3,0,2,4,6,1,7,5]       # inverse permutation
key_p     = [2,4,1,6,3,9,0,8,7,5]   # original key permutation
subkey_p  = [0,1,5,2,6,3,7,4,9,8]   # permutation after removing k0 and k1 
                                    # from the key
sbox_p    = [1,3,2,0]               # permutation for the output of the s-boxes

# Permutates a list (state) according to another list (permutation). 
def perm(state, permutation):
    return list(map(state.__getitem__,permutation))

# Takes a list and expands it by and concatenating two of its permutations 
def expand(bit_list):
    return perm(bit_list,[3,0,1,2]) + perm(bit_list,[1,2,3,0])
    # b0 b1 b2 b3 -> b3 b0 b1 b2 b1 b2 b3 b0

# Takes a four element list (state) and uses it to index an element from the
# specified s-box (box)
def sbox(state,box):
    row = int(state[0] + state[3], 2)
    col = int(state[1] + state[2], 2)
    val = box[row][col]
    return val

# Takes a list (state) and cyclically shifts its elements to the right n times    
def shift_r(state, n):
    a = n % len(state)
    return state[-a:] + state[:-a]

# Takes a list (state) and cyclically shifts its elements to the left n times    
def shift_l(state, n):
    a = n % len(state)
    return state[a:] + state[:a]


# Takes in the sDES key in the form of a string and returns its two subkeys
# in the form of lists of one character ('1's or '0's) strings
def subkeys(key):
    lkey = []
    lkey[:0] = key
    subkey = perm(lkey,key_p)
    rh = subkey[:5]
    lh = subkey[5:]
    subkey1 = perm(shift_l(rh,1)+shift_l(lh,1),subkey_p)
    subkey1.pop(0)
    subkey1.pop(0)
    subkey2 = perm(shift_l(rh,3)+shift_l(lh,3),subkey_p)
    subkey2.pop(0)
    subkey2.pop(0)
    return subkey1,subkey2

# Takes two lists (state and subkey) and applies the sDES feiestel function to
# the state with the subkey
def feistel(state,subkey):
    result = []
    s = []
    rh = state[4:]
    lh = state[:4]
    xored8 = []

    xrh = expand(rh)
    for i in range(len(subkey)):
        xored8.append(str(eval(xrh[i]) ^ eval(subkey[i])))

    s0 = sbox(xored8[:4],S0)
    s1 = sbox(xored8[4:],S1)
    s[:0]  = s0+s1

    ps = perm(s,sbox_p)
    xored4 = []

    for i in range(len(ps)):
        xored4.append(str((eval(lh[i]) ^ eval(ps[i]))))

    return xored4 + rh

# Determines the sDES mode ('E'ncryption or 'D'ecryption), computes the subkeys
# based on the key, and uses them to process the text according to the mode.
def sdes(key,text,mode):
    if mode == 'E':
        sk1,sk2 = subkeys(key)
    elif mode == 'D':
        sk2,sk1 = subkeys(key)
    else:
        exit()

    textl = []
    textl[:0] = text
    step1 = perm(textl, initial_p)
    step2 = feistel(step1,sk1)
    step3 = step2[4:]+step2[:4]
    step4 = feistel(step3,sk2)
    step5 = perm(step4, inverse_p)
    return ''.join(step5)

def main():
    argv = []
    for arg in fileinput.input():
        argv.append(arg)

    mode = argv[0].strip()
    key = argv[1].strip()
    text = argv[2].strip()

    result = sdes(key, text, mode)
    print(result)

if __name__ == "__main__":
    main()
