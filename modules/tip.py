
def tip_calc(total, people, percent=15):
    if total < 0:
        return 0
    new_total = total * (1 + float(percent)/(100.0))
    per_person = new_total/people
    per_person = round(per_person * 4)/4
    while per_person * people < new_total:
        per_person = per_person + 0.25
    new_total = per_person * people
    return "Tip: %.2f\nTotal: %.2f\nSplit: %.2f" %(new_total - total, new_total, per_person)

def tip(args, permisions = {}):
    try:
        if len(args) == 1:
            if args[0][0].lower() == "h":
                return "!tip $total $people $percent(optional)"
        if len(args) == 2:
             return tip_calc(float(args[0]), int(args[1]))
        else:
             return tip_calc(float(args[0]), int(args[1]), int(args[2]))
    except:
        return "invalid numbers"
