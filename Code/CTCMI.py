import secrets

P_256 = int("FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFF".replace(' ', ''), 16)

P_256_N = 275
r_mask = 2 ** 320 - 1

# set as "DEBUG", the hex of a,p,u,v will be printed, set as "RELEASE" if don't need
MODE = "RELEASE"

iteration_a_list, iteration_p_list, iteration_u_list, iteration_v_list = [], [], [], []

def EEA(a: int, p: int):
    if p == 0:
        return 0
    x_last, x_now = 0, 1
    r_last, r_now = p, a
    while r_now != 0:
        q = r_last // r_now
        r_last, r_now = r_now, r_last - q * r_now
        x_last, x_now = x_now, x_last - q * x_now
    if x_last < 0:
        x_last += p
    return x_last


def CT_IMI_CMMI(a: int, p: int, N, INPUT_MODE="INTEGER"):
    u, v, init_p, cnt = 1, 0, p, 0

    for _ in range(N):
        a_lsb, p_lsb = a & 1, p & 1  # get a, p lsb

        # when a, p both odd
        if a_lsb and p_lsb:
            tmp = (p - a) >> 1  # now temp = (p - a) / 2
            if a < tmp:
                tmp = tmp - a  # now temp = (p - 3a) / 2
                if a < tmp:
                    a, p, u, v = a, tmp, u << 1, v - 3 * u  # p >= 5a
                else:
                    a, p, u, v = tmp, a, v - 3 * u, u << 1  # 3a <= p < 5a
            else:
                a, p, u, v = tmp, a, v - u, u << 1  # a < p < 3d
        # when a is odd and p is even
        elif a_lsb and not p_lsb:
            tmp = p >> 1  # now temp = p / 2
            if a < tmp:
                tmp = tmp - a  # now temp = (p - 2a) / 2
                if a < tmp:
                    a, p, u, v = a, tmp, u << 1, v - (u << 1)  # p >= 4a
                else:
                    a, p, u, v = tmp, a, v - (u << 1), u << 1  # 2a <= p < 4a
            else:
                a, p, u, v = tmp, a, v, u << 1  # a < p < 2a
        # when a is even, p is odd
        else:
            half_a, p = a >> 1, p - a  # now half_a = a / 2, p = p - a
            if half_a < p:
                tmp = p - half_a  # now tmp = p - 3/2a
                if half_a < tmp:
                    tmp = tmp - half_a  # now temp = p - 2a
                    if half_a < tmp:
                        a, p, u, v = half_a, tmp, u, (v << 1) - (u << 2)  # p >= 5/2a
                    else:
                        a, p, u, v = tmp, half_a, (v << 1) - (u << 2), u  # 2a <= p < 5/2a
                else:
                    a, p, u, v = half_a, p, u, (v - u) << 1  # 3/2a <= p < 2a
            else:
                a, p, u, v = p, half_a, (v - u) << 1, u  # a < p < 3/2a

        if not (a == 0 and p == 1):
            cnt = cnt + 1

        if MODE == "DEBUG":
            iteration_value = [a, p, u, v]
            tag = ['a', 'p', 'u', 'v']
            store_target = [iteration_a_list, iteration_p_list, iteration_u_list, iteration_v_list]
            for idx, value in enumerate(iteration_value):
                hex_value = hex(value).replace('0x', '').upper()             # if you require signed u, v
                # hex_value = hex(value & r_mask).replace('0x', '').upper()  # if you require unsigned u, v
                store_target[idx].append(hex_value)
                print(tag[idx], ':', hex_value, "\t", 'bit length:', value.bit_length())
            print('---------------------------------', cnt, 'round', '-------------------------------------')

            print("Iteration Finished, the value of v is", hex(v).replace('0x', '').upper())

    """
        the following is simple method to remove 2^n, to promise get the final result
    """

    if INPUT_MODE == "INTEGER":
        for _ in range(N):
            if v & 1:
                v = (v + init_p) >> 1
            else:
                v = v >> 1

    return v % init_p, cnt


if __name__ == "__main__":
    p = P_256
    a = round(secrets.randbelow(p))

    if MODE == "DEBUG":
        print("Set MODE as DEBUG, the value of a,p,u,v will be stored in iteration_x_list")
    elif MODE == "RELEASE":
        print("Set MODE as RELEASE")
    else:
        print("Check the value of MODE!")

    # calculate
    calculate_result = CT_IMI_CMMI(a, p, P_256_N)[0]
    verify_result = EEA(a, p)

    print("Starting Check...")
    assert (calculate_result == verify_result)
    print("Check Pass")

    print("The value of a in this time is", hex(a).replace('0x', '').upper())
