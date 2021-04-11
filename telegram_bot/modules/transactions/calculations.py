def calc_daily_limit_coefficient(daily_transactions, limit):

    daily_total = -1 * sum([tran["delta"] for tran in daily_transactions])
    return (daily_total / limit), daily_total

def map_coefficient_to_advise(coefficient, limit, daily_total):
    remain = daily_total - limit
    if ( coefficient > 1 ):
        return "You have used all your quota for today. Spend More? You'll Over budget."
    if ( coefficient > 0.8 ):
        return "Still on track.You can use only {}. Try to compare prices of things you want to buy.".format(remain)
    if ( coefficient > 0.5 ):
        return "Still on track.You can use only {remain}. Buy only necessary things.".format(remain)
    return None

def get_daily_limit_message(daily_transactions, limit):
    coefficient, daily_total = calc_daily_limit_coefficient(daily_transactions, limit)
    print("coefficient: {}, daily_total: {}".format(coefficient, daily_total))
    message = map_coefficient_to_advise(coefficient, limit, daily_total)
    return message