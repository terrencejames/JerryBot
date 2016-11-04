import math

def choose(args): 
    ans = ""
    try:
        n = int(args[0])
        k = int(args[1])
        ans = str(math.factorial(n) / (math.factorial(k) * math.factorial(n-k)))
    except:
        ans = "invalid input!"
    return ans
