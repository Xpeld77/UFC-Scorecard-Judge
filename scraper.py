import requests
from bs4 import BeautifulSoup

# Helper function to parse strings like "x of x"
def parse_stat(stat_string):
    parts = stat_string.split(' of ')
    landed = int(parts[0])
    attempted = int(parts[1]) if len(parts) > 1 else landed
    return landed, attempted

# Helper function to parse strings like "M:SS"
def parse_time_to_seconds(time_string):
    if ':' not in time_string:
        return int(time_string) # Handles cases where it might just be '0'
    minutes, seconds = map(int, time_string.split(':'))
    return (minutes * 60) + seconds

# Get html content of the page
def scrape_fight_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Get fighter names
        name_elements = soup.find_all('h3', class_='b-fight-details__person-name')
        if len(name_elements) < 2:
            raise ValueError("Could not find fighter names.")
        fighter1_name = name_elements[0].text.strip()
        fighter2_name = name_elements[1].text.strip()
        print(f"Fetching stats for: {fighter1_name} vs. {fighter2_name}\n")

        #Find all the tables on the page
        tables = soup.find_all('table')

        #Check if there is round by round table
        if len(tables) < 2:
            print("Could not find the per-round stats table")
        else:
            round_stats_table = tables[1]

            # Extract data from each row(round) of the table and store it in a list
            rounds_data = []

            # Get all the table rows
            for row in round_stats_table.find_all('tr')[1:]:
                # Get all the cells in that row
                cells = row.find_all('td')
                
                # Get cell data
                if len(cells) > 0:
                    p_tags_kd = cells[1].find_all('p')
                    p_tags_sig_str = cells[2].find_all('p')
                    p_tags_td = cells[5].find_all('p')
                    p_tags_sub = cells[7].find_all('p')
                    p_tags_control = cells[9].find_all('p')

                    # Clean up the data
                    f1_knockdowns = int(p_tags_kd[0].text.strip())
                    f2_knockdowns = int(p_tags_kd[1].text.strip())

                    f1_sig_str_landed, f1_sig_str_attempted = parse_stat(p_tags_sig_str[0].text.strip())
                    f2_sig_str_landed, f2_sig_str_attempted = parse_stat(p_tags_sig_str[1].text.strip())

                    f1_td_landed, f1_td_attempted = parse_stat(p_tags_td[0].text.strip())
                    f2_td_landed, f2_td_attempted = parse_stat(p_tags_td[1].text.strip())

                    f1_sub_attempts, _ = parse_stat(p_tags_sub[0].text.strip())
                    f2_sub_attempts, _ = parse_stat(p_tags_sub[1].text.strip())

                    f1_control_time = parse_time_to_seconds(p_tags_control[0].text.strip())
                    f2_control_time = parse_time_to_seconds(p_tags_control[1].text.strip())

                    
                    round_info = {
                        "fighter1": {
                            "knockdowns": f1_knockdowns,
                            "sig strikes landed": f1_sig_str_landed,
                            "sig strikes attempted": f1_sig_str_attempted,
                            "takedowns landed": f1_td_landed,
                            "takedowns attempted": f1_td_attempted,
                            "sub attempts": f1_sub_attempts,
                            "control time": f1_control_time
                        },
                        "fighter2": {
                            "knockdowns": f2_knockdowns,
                            "sig strikes landed": f2_sig_str_landed,
                            "sig strikes attempted": f2_sig_str_attempted,
                            "takedowns landed": f2_td_landed,
                            "takedowns attempted": f2_td_attempted,
                            "sub attempts": f2_sub_attempts,
                            "control time": f2_control_time
                        }
                    }
                    rounds_data.append(round_info)

            return fighter1_name, fighter2_name, rounds_data
            
    # Exceptions
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    except (ValueError, IndexError) as e:
        print(f"Error parsing the page data: {e}. The page structure might be different than expected.")