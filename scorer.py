def score_round(round_data, fighter1_name, fighter2_name):
    """
    Scores a single round in a tuple based on UFC criteria.
    """
    f1_stats = round_data['fighter1']
    f2_stats = round_data['fighter2']

    # --- Scoring Logic ---

    # Check for a 10-9 or 10-10 round
    
    # striking accuracy 
    f1_strike_acc = f1_stats['sig strikes landed'] / f1_stats['sig strikes attempted'] if f1_stats['sig strikes attempted'] > 0 else 0
    f2_strike_acc = f2_stats['sig strikes landed'] / f2_stats['sig strikes attempted'] if f2_stats['sig strikes attempted'] > 0 else 0
    
    # takedown accuracy
    f1_td_acc = f1_stats['takedowns landed'] / f1_stats['takedowns attempted'] if f1_stats['takedowns attempted'] > 0 else 0
    f2_td_acc = f2_stats['takedowns landed'] / f2_stats['takedowns attempted'] if f2_stats['takedowns attempted'] > 0 else 0

    # Striking points
    f1_striking_points = (f1_stats['knockdowns'] * 4) + (f1_stats['sig strikes landed'] * 0.25)  + (f1_strike_acc * 0.5)
    f2_striking_points = (f2_stats['knockdowns'] * 4) + (f2_stats['sig strikes landed'] * 0.25)  + (f2_strike_acc * 0.5)

    # Grappling points
    f1_grappling_points = (f1_stats['takedowns landed'] * 1.5) + (f1_td_acc * 0.5) + (f1_stats['sub attempts'] * 2) + (f1_stats['control time'] * 0.01) 
    f2_grappling_points = (f2_stats['takedowns landed'] * 1.5) + (f2_td_acc * 0.5) + (f2_stats['sub attempts'] * 2) + (f2_stats['control time'] * 0.01)
    
    # Deduct points if there is ineffective control time and less sig strikes landed
    if f1_stats['control time'] > 60 and f1_stats['sig strikes landed'] < f2_stats['sig strikes landed']:
        f1_grappling_points -= 2
    if f2_stats['control time'] > 60 and f2_stats['sig strikes landed'] < f1_stats['sig strikes landed']:
        f2_grappling_points -= 2

    f1_total_points = f1_striking_points + f1_grappling_points
    f2_total_points = f2_grappling_points + f2_striking_points

    # For debugging to see the point breakdown each round
    #print(f"\n{fighter1_name} Points: {f1_total_points}")
    #print(f"{fighter2_name} Points: {f2_total_points}")

    # Check for a clear 10-8 round (dominant)
    # Condition 1: Multiple knockdowns
    if f1_stats['knockdowns'] >= 3:
        return ((10, 8), "due to multiple knockdowns")
    if f2_stats['knockdowns'] >= 3:
        return ((8, 10), "due to multiple knockdowns")
    
    # Condition 2: One Knockdown and significant striking advantage
    if f1_stats['knockdowns'] >= 1 and f1_stats['sig strikes landed'] > (f2_stats['sig strikes landed'] * 2):
        return ((10, 8), "due to a knockdown and significant striking advantage")
    if f2_stats['knockdowns'] >= 1 and f2_stats['sig strikes landed'] > (f1_stats['sig strikes landed'] * 2):
        return ((8, 10), "due to a knockdown and significant striking advantage")
    
    # Condition 3: One knockdown and significant grappling advantage 
    if f1_stats['knockdowns'] >= 1 and f1_stats['takedowns landed'] >= 2 and f1_stats['control time'] > 60 and f1_stats['sub attempts'] > (f2_stats['sub attempts'] * 2):
        return ((10, 8), "due to a knockdown and significant grappling control")
    if f2_stats['knockdowns'] >= 1 and f2_stats['takedowns landed'] >= 2 and f2_stats['control time'] > 60 and f2_stats['sub attempts'] > (f1_stats['sub attempts'] * 2):
        return ((8, 10), "due to a knockdown and significant grappling control")
    
    # Condition 4: Massive striking or control disparity
    strike_diff = abs(f1_stats['sig strikes landed'] - f2_stats['sig strikes landed'])
    if strike_diff > 45: 
        if f1_stats['sig strikes landed'] > f2_stats['sig strikes landed']:
            return ((10, 8), "due to a massive striking disparity")
        else:
            return ((8, 10), "due to a massive striking disparity") 
        
    if f1_stats['control time'] > 210 and f1_stats['takedowns landed'] > 0:
        return ((10, 8), "due to overwhelming grappling control")
    if f2_stats['control time'] > 210 and f2_stats['takedowns landed'] > 0:
        return ((8, 10), "due to overwhelming grappling control")

    # Condition 5: Significant grappling control with a large striking disparity (ground and pound)
    if f1_stats['control time'] > 150 and f1_stats['sig strikes landed'] > (f2_stats['sig strikes landed'] + 20):
        return ((10, 8), "due to dominant grappling and ground-and-pound")
    if f2_stats['control time'] > 150 and f2_stats['sig strikes landed'] > (f1_stats['sig strikes landed'] + 20):
        return ((8, 10), "due to dominant grappling and ground-and-pound")
    
    # --- Final Decision ---
    if f1_total_points > f2_total_points:
        if f1_striking_points > f2_striking_points:
            reason = "due to a striking advantage"
        elif f1_grappling_points > f2_grappling_points:
            reason = "due to a grappling advantage"
        else:
            reason = "due to a well rounded striking and grappling advantage"
        return ((10, 9), reason)
    elif f2_total_points > f1_total_points:
        if f2_striking_points > f1_striking_points:
            reason = "due to a striking advantage"
        elif f2_grappling_points > f1_grappling_points:
            reason = "due to a grappling advantage"
        else:
            reason = "due to a well rounded striking and grappling advantage"
        return ((9, 10), reason)
    else:
        reason = "the fight was too close to call"
        return ((10, 10), reason) 
    
    