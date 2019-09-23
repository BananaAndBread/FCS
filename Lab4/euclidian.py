def egcd(a, b):
    x2 = 1
    y2 = 0
    x1 = 0
    y1 = 1
    r2=b
    r1=a
    i=1
    print("step 0)")
    print("initializing remainder", r1)
    print("coeff", y1, x1)
    while r1!= 0:
        print(f"step {i})")
        print(f"pair {r2, r1}")
        i=i+1
        q = r2 // r1
        r = r2 % r1
        x = x2 - (q * x1)
        y = y2 - (q * y1)
        print("remainder", r)
        print("coeff", y,x)
        r2 = r1
        r1 = r
        x2 = x1
        y2 = y1
        x1 = x
        y1 = y

    return r2, y2, x2

print(egcd(91, 26))
