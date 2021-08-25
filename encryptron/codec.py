# Codec Scrambling and Permutations

def check_hex_perm(perm):
    if len(perm) != 16:
        return False
    s = set([i for i in perm]).intersection(set([hex(i)[2:] for i in range(16)]))
    return len(s) == 16

def apply_hex_perm(lst, perm):
    # check integrity of lst and perm
    if len(lst) != 16 or len(perm) != 16:
        return False
    if not check_hex_perm(perm):
        return []

    perm_lst = [int(i, 16) for i in perm]
    return [lst[i] for i in perm_lst]


# Generic Encoding Methods

def hex_encode(text, codec, filter=(lambda x: x)): # codec is a 16 element list
    outstr = ""
    for char in text:
        n = filter(ord(char))
        outstr += codec[n>>4] + codec[n%16]
    return outstr

def hex_decode(crypted, codec, filter=(lambda x: x)):
    # notice that this filter is the inverse of the encoding filter
    outstr = ""
    crypts = list(crypted)
    vals = []

    if len(crypts) % 2:
        pass # Something is wrong, crypts should be even in size

    for hexbit in crypts:
        try:
            vals.append(codec.index(hexbit))
        except IndexError:
            pass # Invalid Character Found

    for i in range(len(vals)>>1):
        n = filter((vals[2*i]<<4) + vals[2*i+1])
        outstr += chr(n)

    return outstr

# Allows ascii encoding of hex Permutations

def key_to_perm(key):
    p = [hex(i)[2:] for i in range(16)]
    i = 0
    for char in key:
        n = (ord(char) + i) % 256
        if n%17==0: # this is when a == b
            continue
        # a byte is two hex numbers
        a = n>>4 # the first hex number
        b = n%16 # the second hex number
        # we'll sway these two hex numbers
        m = min(a,b)
        n = max(a,b)
        fst = p.pop(m)
        snd = p.pop(n-1)
        p.insert(m, snd)
        p.insert(n, fst)
        i += 41  # scrambler

    return "".join(p)


# Tools to help scramble up code (in case no other ciphers to use)
# This is mandatory to protect the integrity of the codec (from users)

_tribonacci = [0, 0, 1]
def tribonacci_256(n):
    while n >= len(_tribonacci):
        _tribonacci.append(sum(_tribonacci[-3:]) % 256)
    return _tribonacci[n]

_fibonacci = [0, 1]
def fibonacci_256(n):
    while n >= len(_fibonacci):
        _fibonacci.append((_fibonacci[-2] + _fibonacci[-1]) % 256)
    return _fibonacci[n]

_lucas = [2, 1]
def lucas_256(n):
    while n >= len(_lucas):
        _lucas.append((_lucas[-2] + _lucas[-1]) % 256)
    return _lucas[n]

num_gen = {
    "tribonacci": tribonacci_256,
    "fibonacci": fibonacci_256,
    "lucas": lucas_256
}

# The Whitespace Codec (Alternative: 0x2800 empty braile works too)
whitespace_codec = [0x20, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006, 0x2007, 0x2008, 0x2009, 0x200a, 0x2028, 0x205f, 0x2063, 0x3000]

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


@static_vars(pos=0)
def trib_filter(n, inverse=False):
    if n < 0:
        trib_filter.pos = -n-1
        return 0
    trib_filter.pos += 1
    return (n + (-1 if inverse else 1) * num_gen['tribonacci'](trib_filter.pos))%256


@static_vars(pos=0)
def fib_filter(n, inverse=False):
    if n < 0:
        fib_filter.pos = -n-1
        return 0
    fib_filter.pos += 1
    return (n + (-1 if inverse else 1) * num_gen['fibonacci'](fib_filter.pos))%256


@static_vars(pos=0)
def lucas_filter(n, inverse=False):
    if n < 0:
        lucas_filter.pos = -n-1
        return 0
    lucas_filter.pos += 1
    return (n + (-1 if inverse else 1) * num_gen['lucas'](lucas_filter.pos))%256

num_gen_filters = {
    "tribonacci": trib_filter,
    "fibonacci": fib_filter,
    "lucas": lucas_filter
}

def reset_num_gen_filters():
    for f in num_gen_filters.values():
        f(-1)

# Key takes precedence to Perm since only one will be used
def ws_encode(text, filter="", key=None, perm=None):
    reset_num_gen_filters()
    codec = [chr(i) for i in whitespace_codec]
    if key:
        codec = apply_hex_perm(codec, key_to_perm(key))
    elif perm:
        c = apply_hex_perm(codec, perm)
        if c:
            codec = c
    return " " + chr(0x200a) + hex_encode(text, codec, filter=num_gen_filters.get(filter, num_gen_filters['tribonacci']))+ chr(0x200a) + " "

# Key takes precedence to Perm since only one will be used
def ws_decode(crypted, filter="", key=None, perm=None):
    reset_num_gen_filters()
    codec = [chr(i) for i in whitespace_codec]
    lst = list(crypted)
    while lst:
        if lst.pop(0) == chr(0x200a):
            break
    while lst:
        if lst.pop() == chr(0x200a):
            break
    crypted = "".join(lst)

    if not crypted:
        return ""

    if key:
        codec = apply_hex_perm(codec, key_to_perm(key))
    elif perm:
        c = apply_hex_perm(codec, perm)
        if c:
            codec = c
    inv_filter = lambda n : num_gen_filters.get(filter, num_gen_filters['tribonacci'])(n, inverse=True)
    return hex_decode(crypted, codec, filter=inv_filter)
