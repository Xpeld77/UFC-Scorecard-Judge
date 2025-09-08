from scorer import score_round
from scraper import scrape_fight_data
def main():
    print("--- Welcome to the UFC Scorecard Judge ---")
    fight_url = input("Enter the UFCStats.com fight details URL: ")

    # 1. Scrape data from the URL
    fighter1_name, fighter2_name, all_rounds_data = scrape_fight_data(fight_url)

    # Exit if scraping fails
    if not all_rounds_data:
        print("Could not retrive fight data. Please check the URL and try again.")
        return
    print(f"\n --- Scoring: {fighter1_name} vs. {fighter2_name} ---")

    # 2. Score each round and keep a running total
    fighter1_total_score = 0
    fighter2_total_score = 0

    for i, round_data in enumerate(all_rounds_data):
        round_num = i + 1
        (f1_score, f2_score), reason = score_round(round_data, fighter1_name, fighter2_name)
        formatted_reason = reason.capitalize()
        print(f"\nRound {round_num} Score: {fighter1_name} {f1_score} - {f2_score} {fighter2_name} ({formatted_reason})")
        fighter1_total_score += f1_score
        fighter2_total_score += f2_score
    
    # 3. Announce the winner
    print("\n --- OUR FINAL SCORE ---")
    print(f"{fighter1_name} {fighter1_total_score} - {fighter2_total_score} {fighter2_name}")

    if fighter1_total_score > fighter2_total_score:
        print(f"\nThe winner is {fighter1_name}!")
    elif fighter2_total_score > fighter1_total_score:
        print(f"\nThe winner is {fighter2_name}!")
    else:
        print("\nThe fight is a draw!")

if __name__ == "__main__":
    main()
    