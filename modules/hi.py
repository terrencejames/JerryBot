import permissions as p

def hi(args, perms = {}):
    full_name = perms[p.USER_NAME]
    first = full_name.split()[0]
    return "Hi, " + first + "!"