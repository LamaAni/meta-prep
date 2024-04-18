#  %% Reverse
x = 1024
val = 0

while x > 0:
    print(x, bin(x)[2:], val, bin(val)[2:])
    val = (val << 1) + (x & 1)
    x = x >> 1
    
print(x, bin(x)[2:], val, bin(val)[2:])
