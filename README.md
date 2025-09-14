
# UFC Scorecard Judge
A command-line application that acts as an unbiased UFC judge. This tool scrapes round-by-round fight data from UFCStats.com and scores the contest based on a detailed, rule-based logic engine inspired by the official Unified Rules of MMA.

The goal of this project is to provide an objective, data-driven analysis of MMA fights, allowing users to compare a statistical scorecard against the official decisions, especially in famously controversial bouts.

## How It Works
The application operates in four main stages:

Scrape: It takes a fight details URL from UFCStats.com as input and uses the requests and BeautifulSoup libraries to fetch and parse the raw HTML of the webpage.

Process: It navigates the parsed HTML to find the round-by-round statistics table, extracting key metrics for each fighter, including knockdowns, significant strikes (landed and attempted), takedowns, submission attempts, and control time.

Score: For each round, it passes the structured data to a sophisticated scoring engine. This engine first checks for conditions of clear dominance to award a 10-8 round. If no dominance is found, it uses a weighted point system to determine the winner of a competitive 10-9 round.

Display: It presents a final scorecard in the terminal, complete with a justification for why each round was scored a certain way.

## Scoring Logic
The scoring engine is designed to mirror the decision-making process of a real MMA judge, prioritizing clear dominance before analyzing a competitive round. The logic is executed in two phases:

1. The 10-8 Round (Clear Dominance)
First, the program checks for clear, overwhelming dominance. A round is scored 10-8 if any of the following high-impact conditions are met:

- Multiple Knockdowns: The fighter scores two or more knockdowns.

- Knockdown + Overwhelming Offense: The fighter scores a knockdown AND more than doubles their opponent's significant strike total.

- Knockdown + Dominant Grappling: The fighter scores a knockdown, lands multiple takedowns, and maintains significant control time.

- Massive Striking Disparity: An extreme difference in significant strikes landed (e.g., a differential of 45+ strikes).

- Overwhelming Grappling Control: A fighter maintains more than 3.5 minutes (210 seconds) of control time.

- Sustained Ground-and-Pound: The fighter achieves significant control time (2.5+ minutes) while also landing a high volume of ground strikes (20+ more than the opponent).

2. The 10-9 Round (Competitive Edge)
If no 10-8 conditions are met, the round is scored using a weighted point system to determine which fighter had the more effective offense. Points are awarded based on the following metrics:

- Impact: Knockdowns and submission attempts are heavily weighted.

- Volume: Significant strikes landed contribute the core of the striking points.

- Control: Takedowns landed and total control time form the basis of the grappling score.

- Efficiency (Bonus): A bonus is added for high accuracy in both significant strikes and takedowns, rewarding effective offense over wasted motion.

- Ineffective Control (Penalty): To counter "lay and pray," a point penalty is applied if a fighter accumulates significant control time but gets out-struck, ensuring control is only rewarded when it's used effectively.

- The fighter with the higher point total at the end of the calculation wins the round 10-9. If the points are equal, the round is scored a 10-10 draw.

## Features
Automated Data Scraping: Fetches detailed stats for any fight on UFCStats.com with just a URL.

Nuanced Scoring Logic: Distinguishes between dominant (10-8) and competitive (10-9) rounds.

Justified Decisions: Provides a text reason for every round's score (e.g., "Due to a striking advantage," "Due to overwhelming grappling control").

Controversy Analysis: Built and tested to score famously disputed fights and provide an objective, data-driven perspective.

## Getting Started
To get a local copy up and running, follow these simple steps.

## Prerequisites
Make sure you have Python 3 and pip installed on your system.

## Installation

1. On the main GitHub repository page, click the green <> Code button.

2. Select Download ZIP.

3. Extract the contents of the ZIP file to a location on your computer.

4. Open your terminal and navigate into the extracted folder (it will be named UFC-Scorecard-Judge-main)
  
5. Install the required libraries:
```
pip install requests beautifulsoup4
```
## Usage
Run the main application file from your terminal:
```
python UFCScorecardJudge.py
```
The program will then prompt you to enter a valid UFC Stats fight details URL.

Example URL:
```
http://ufcstats.com/fight-details/e60e53bdc614a0af
```
## Example Output
Here is the program's analysis of the famously controversial Mauricio "Shogun" Rua vs. Lyoto Machida I fight, correctly overturning the official decision.
```
--- Welcome to the UFC Scorecard Judge ---
Please enter the UFCStats.com fight details URL: http://ufcstats.com/fight-details/e60e53bdc614a0af

 --- Scoring: Lyoto Machida vs. Mauricio Rua ---

Round 1 Score: Lyoto Machida 9 - 10 Mauricio Rua (Due to a striking advantage)

Round 2 Score: Lyoto Machida 9 - 10 Mauricio Rua (Due to a striking advantage)

Round 3 Score: Lyoto Machida 9 - 10 Mauricio Rua (Due to a striking advantage)

Round 4 Score: Lyoto Machida 9 - 10 Mauricio Rua (Due to a striking advantage)

Round 5 Score: Lyoto Machida 9 - 10 Mauricio Rua (Due to a striking advantage)

 --- OUR FINAL SCORE ---
Lyoto Machida 45 - 50 Mauricio Rua

The winner is Mauricio Rua!
```
