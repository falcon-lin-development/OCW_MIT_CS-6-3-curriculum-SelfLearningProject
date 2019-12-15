stock = {
    "Dale": 0,
    "JCN": 1,
    "Macroware": 2,
    "Pear": 3,
}
stocks = ["Dale", "JCN", "Macroware", "Pear"]
start = [12, 10, 18, 15]
end = [39, 13, 47, 45]
limit = [3, "infinity", 2, 1]


def save_dec(n):
    if n == "infinity":
        return "infinity"
    else:
        return n - 1


def have_stock(n):
    if n == "infinity" or n > 0:
        return True
    else:
        return False


def _calc_purchase(total, start, end, limit=None, debug=0):  # O(total * #stocks)
    result = [(0, [0, 0, 0, 0]), ]
    if limit:
        lim = limit[:]
    for cash in range(1, total + 1):
        choices = []
        # c0 buy nothing
        if cash > 0:
            last_profit, last_purchases = result[cash - 1]
            choices.append((last_profit + 1, last_purchases))
        # c1-n buy one stock
        for s in range(len(start)):
            """No correct algorithm, the only thing we can do is consider the quantity in every trial.
            As a result, we recalculate everything in every step.
            """
            if limit:
                if not have_stock(lim[s]):
                    choices.append((0, None))  # No enough stocks for an option
                    continue
            if cash >= start[s]:
                last_profit, last_purchases = result[cash - start[s]]
                current_profit = last_profit + end[s]
                new_purchases = last_purchases[:]
                new_purchases[s] += 1
                choices.append((current_profit, new_purchases))
            else:
                choices.append((0, None))  # No enough money for an option

        choice = max(choices)
        if limit:
            choice_index = choices.index(choice)
            if choice_index != 0:
                lim[choice_index - 1] = save_dec(lim[choice_index - 1])

        if debug: print lim
        result.append(choice)

    return result


for i, e in enumerate(_calc_purchase(120, start, end, limit)):
    print i, e
