
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

initial_p = [1,5,2,0,3,7,4,6]       
inverse_p = [3,0,2,4,6,1,7,5]       
key_p     = [2,4,1,6,3,9,0,8,7,5]   
subkey_p  = [0,1,5,2,6,3,7,4,9,8]   
                                    
sbox_p    = [1,3,2,0]               


def perm(state, permutation):
    return list(map(state.__getitem__,permutation))

 
def expand(bit_list):
    return perm(bit_list,[3,0,1,2]) + perm(bit_list,[1,2,3,0])



def sbox(state,box):
    row = int(state[0] + state[3], 2)
    col = int(state[1] + state[2], 2)
    val = box[row][col]
    return val
   
def shift_r(state, n):
    a = n % len(state)
    return state[-a:] + state[:-a]
   
def shift_l(state, n):
    a = n % len(state)
    return state[a:] + state[:a]


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
