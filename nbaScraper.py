from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

teamToState = {"Miami": "fl", "Oklahoma City": "ok", "New Orleans": "la", "Atlanta": "ga"}


def main():
    scrapeNBASite()

def scrapeNBASite():

    soup = BeautifulSoup(open("schedule.html"), 'html.parser')
    main_container = soup.find_all("div", {"class": "ScheduleDay_sd__2bdg0"})
    results = []
    for container in main_container:
        children = container.findChildren("div" , recursive=False)
        date = ""
        gamesCount = ""
        teams = []
        for child in children:
            dateDiv = child.find("h4", {"class": "ScheduleDay_sdDay__nM9By"})
            if (dateDiv):
                date_time_obj = datetime.strptime(dateDiv.text, "%A, %B %d")
                if date_time_obj.month > 4:
                    date_time_obj = date_time_obj.replace(year = 2022)
                else: 
                    date_time_obj = date_time_obj.replace(year = 2023)
                date = date_time_obj
            gamesTotal = child.find("h6", {"class": "ScheduleDay_sdWeek__GsFqu"})
            if (gamesTotal):
                gamesCount = gamesTotal.text
            gamesOnDay = child.find("div", {"class": "ScheduleDay_sdGames__1PJah"})
            if (gamesOnDay):
                for game in gamesOnDay.findChildren("div", recursive=False):
                    competingGames = game.find("div", {"class": "pb-5 xl:pb-0 min-w-1/2 xl:min-w-6/10"})
                    if (competingGames):
                        team1 = ""
                        team2 = ""
                        for div in competingGames:
                            if (team1 == ""):
                                team1 = div.text
                            else:
                                team2 = div.text

                        teams.append(f"{team1} vs. {team2}")

        for key in teamToState.keys():
            if (any(f"vs. {key}" in team for team in teams)):
                # print(f"{date}")
                playing = ""
                # print(f"Matchups: {teams}")
                for matchup in teams:
                    if f"vs. {key}" in matchup:
                        playing = matchup
                        # print(matchup)
                # print(f"Match for: {teamToState[key]}")
                # print()
                dayBefore = date - timedelta(hours=24)
                dayAfter = date +  timedelta(hours=24)
                formattedBefore = dayBefore.strftime("%m-%d-%Y")
                formattedAfter = dayAfter.strftime("%m-%d-%Y")
                results.append({
                    "date": f"{formattedBefore}-to-{formattedAfter}",
                    "state": teamToState[key],
                    "city": key,
                    "teams": playing
                })
    return results
if __name__ == "__main__":
    main()