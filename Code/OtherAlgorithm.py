import math
def Test_BEEA(a: int, p: int):
    u, v = a, p
    x1, x2 = 1, 0
    cnt = 0
    while u != 1 and v != 1:
        while u & 1 == 0:
            cnt += 1
            u >>= 1
            if x1 & 1 == 0:
                x1 >>= 1
            else:
                x1 = (x1 + p) >> 1
        while v & 1 == 0:
            cnt += 1
            v >>= 1
            if x2 & 1 == 0:
                x2 >>= 1
            else:
                x2 = (x2 + p) >> 1
        if u >= v:
            u, x1 = u - v, x1 - x2
        else:
            v, x2 = v - u, x2 - x1
        cnt += 1
    if u == 1:
        return x1 % p, cnt
    return x2 % p, cnt

def Test_HBEEA(a: int, p: int):
    x, y, u, v, cnt = a, p, 0, 0, 0
    while x & 1 == 0 and y & 1 == 0:
        x >>= 1
        y >>= 1
    if x & 1 == 0:
        u, v = y, x
        A, C, B, D = 0, 1, 1, 0
    else:
        u, v = x, y
        A, C, B, D = 1, 0, 0, 1
    while v != 0:
        while v & 1 == 0:
            cnt += 1
            v >>= 1
            if C & 1 == 0 and D & 1 == 0:
                C >>= 1
                D >>= 1
            else:
                C = (C + y) >> 1
                D = (D - x) >> 1
        if u >= v:
            u, v = v, u - v
            A, C, B, D = C, A - C, D, B - D
        else:
            v = v - u
            C, D = C - A, D - B
        cnt += 1
    return A % y, cnt


def Test_Stein(a: int, b: int):  # ax+by=gcd(a,b), 在给出ab之后，得出裴蜀定理中的三个变量xyr
    x1, x2, x3 = 1, 0, b
    y1, y2, y3 = 0, 1, a
    cnt = 0
    while x3 != 1 or y3 != 1:
        cnt += 1
        if x3 & 1 == 0:
            if x1 & 1 == 0 and x2 & 1 == 0:
                x1, x2, x3 = x1 >> 1, x2 >> 1, x3 >> 1
            else:
                x1 += a
                x2 -= b
        elif y3 & 1 == 0:
            if y1 & 1 == 0 and y2 & 1 == 0:
                y1, y2, y3 = y1 >> 1, y2 >> 1, y3 >> 1
            else:
                y1 += a
                y2 -= b
        elif x3 > y3:
            x1, x2, x3 = x1 - y1, x2 - y2, x3 - y3
        else:
            y1, y2, y3 = y1 - x1, y2 - x2, y3 - x3
    if x3 == 1:
        return x2 % b, cnt
    else:
        return y2 % b, cnt


def Test_P_stein(a: int, b: int):  # 减少了两个临时变量，开销比stein算法小
    x1, x3 = 1, a
    y1, y3 = 0, b
    cnt = 0
    while x3 != 1 or y3 != 1:
        cnt += 1
        if x3 & 1 == 0:
            if x1 & 1 == 0:
                x1, x3 = x1 >> 1, x3 >> 1
            else:
                x1 += b
        elif y3 & 1 == 0:
            if y1 & 1 == 0:
                y1, y3 = y1 >> 1, y3 >> 1
            else:
                y1 += b
        elif x3 > y3:
            x1, x3 = x1 - y1, x3 - y3
        else:
            y1, y3 = y1 - x1, y3 - x3
    if x3 == 1:
        return x1 % b, cnt
    else:
        return y1 % b, cnt

def Test_MI(a: int, p: int):  # 蒙哥马利模乘和模逆相结合的改进算法
    u, v, r, s = p, a, 0, 1
    init_p = p
    k = 0
    cnt = 0
    while v > 0:
        cnt += 1
        if u & 1 == 0:
            u, s = u >> 1, s << 1
        elif v & 1 == 0:
            v, r = v >> 1, r << 1
        elif u > v:
            u, r, s = (u - v) >> 1, r + s, s << 1
        else:
            v, s, r = (v - u) >> 1, r + s, r << 1
        k = k + 1
    while r >= p:
        r = r - p
    r = p - r
    return r % init_p, cnt

def fastExpMod(b, e, m):
    result = 1
    while e != 0:
        if (e&1) == 1:
            result = (result * b) % m
        e >>= 1
        b = (b*b) % m
    return result

def FLT(a, p):
    return fastExpMod(a, p-2, p)

def BY(a, p):
    l = math.floor((49 * p.bit_length() + 57) / 17)
    u, v, q, r, delta = a, p, 0, 1, 1
    for i in range(l):
        z = u & 1
        s = 1 if -delta > 0 else -1
        s_times_z = s * z
        delta = 1 + (1 - (s_times_z << 1)) * delta
        u, v = (u + (1 - (s_times_z << 1) * z * v)) >> 1, v ^ s_times_z * (v ^ u)
        q, r = (q ^ s_times_z * (q ^ r)) << 1, (1 - (s_times_z << 1)) * z * q + r
    return q

def SI_MI(a,p):
    l = 2 * p.bit_length()
    u, v, q, r = a, p, 0, 1
    for i in range(l):
        t1, t2 = v - u, q - r
        if u & 1 and v & 1:
            t1, r = t1 >> 1, r << 1
            if u > t1:
                q, r, v, u = r, t2, u, t1
            else:
                q, r, v, u = t2, r, t1, u
        elif u & 1:
            v, t2 = v >> 1, t2 << 1
            if t1 > v:
                r, q, u, v = q, t2, v, t1
            else:
                q, r, v, u = q, t2, v, t1
        else:
            u, t2 = u >> 1, t2 << 1
            if t1 > u:
                r, q, u, v = r, t2, u, t1
            else:
                q, r, v, u = r, t2, v, t1
    return q