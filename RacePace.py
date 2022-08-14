from textwrap import indent
import fastf1 as ff1
from fastf1 import plotting

import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import cm

import numpy as np

import json
import requests


def makeRaceGraph():
    # Enable the cache
    ff1.Cache.enable_cache("cache/")

    season, race, raceName = getLastRace()
    laps = getLaps(season, race)
    lapsCleaned = cleanLaps(laps)

    drivers_to_visualize = getTopFive(season, race)

    # To make sure we won't get any equally styled lines when comparing teammates
    visualized_teams = []

    # Make plot a bit bigger
    plt.rcParams["figure.figsize"] = [10, 10]

    # Create 2 subplots
    fig, ax = plt.subplots(2, gridspec_kw={"height_ratios": [3, 1], "hspace": 0.3})
    ##############################
    #
    # Strategy graph
    #
    ##############################

    driver_stints = (
        laps[["Driver", "Stint", "Compound", "LapNumber"]]
        .groupby(["Driver", "Stint", "Compound"])
        .count()
        .reset_index()
    )

    driver_stints = driver_stints.rename(columns={"LapNumber": "StintLength"})

    driver_stints = driver_stints.sort_values(by=["Stint"])

    compound_colors = {
        "SOFT": "#FF3333",
        "MEDIUM": "#FFF200",
        "HARD": "#EBEBEB",
        "INTERMEDIATE": "#39B54A",
        "WET": "#00AEEF",
    }

    for driver in drivers_to_visualize:
        stints = driver_stints.loc[driver_stints["Driver"] == driver]

        previous_stint_end = 0
        for _, stint in stints.iterrows():
            plt.barh(
                [driver],
                stint["StintLength"],
                left=previous_stint_end,
                color=compound_colors[stint["Compound"]],
                edgecolor="black",
            )

            previous_stint_end = previous_stint_end + stint["StintLength"]

    # Set title
    ax[1].set_title(f"Race strategy")

    # Set x-label
    ax[1].set_xlabel("Laps")

    # Invert y-axis
    ax[1].invert_yaxis()

    # Remove frame from plot
    ax[1].spines["top"].set_visible(False)
    ax[1].spines["right"].set_visible(False)
    ax[1].spines["left"].set_visible(False)

    ##############################
    #
    # Lap-by-lap racepace comparison
    #
    ##############################
    for driver in drivers_to_visualize:
        driver_laps = lapsCleaned.pick_driver(driver)[
            ["LapNumber", "LapTimeSeconds", "Team"]
        ]

        # Select all the laps from that driver
        driver_laps = driver_laps.dropna()

        # Extract the team for coloring purploses
        team = pd.unique(driver_laps["Team"])[0]

        # X-coordinate is the lap number
        x = driver_laps["LapNumber"]

        # Y-coordinate a smoothed line between all the laptimes
        poly = np.polyfit(driver_laps["LapNumber"], driver_laps["LapTimeSeconds"], 5)
        y_poly = np.poly1d(poly)(driver_laps["LapNumber"])

        # Make sure that two teammates don't get the same line style
        linestyle = "-" if team not in visualized_teams else ":"

        # Plot the data
        ax[0].plot(
            x,
            y_poly,
            label=driver,
            color=ff1.plotting.team_color(team),
            linestyle=linestyle,
        )

        # Append labels
        ax[0].set(ylabel="Laptime (s)")
        ax[0].set(xlabel="Lap")

        # Set title
        ax[0].set_title(f"Smoothed racepace\n{raceName}")

        # Generate legend
        ax[0].legend()

        # Add the team to the visualized teams variable so that the next time the linestyle will be different
        visualized_teams.append(team)

    path = "./images/racepace_comparison.png"
    plt.savefig(path, dpi=300)
    print('Figure saved (racepace_comparison.png)')
    plt.close()
    return path


def cleanLaps(laps):
    # To get accurate laps only, we exclude in- and outlaps
    laps = laps.loc[(laps["PitOutTime"].isnull() & laps["PitInTime"].isnull())]

    # Also, we remove outliers since those don't represent the racepace,
    # using the Inter-Quartile Range (IQR) proximity rule
    q75, q25 = laps["LapTimeSeconds"].quantile(0.75), laps["LapTimeSeconds"].quantile(
        0.25
    )

    intr_qr = q75 - q25

    laptime_max = q75 + (1.5 * intr_qr)  # IQR proximity rule: Max = q75 + 1,5 * IQR
    laptime_min = q25 - (1.5 * intr_qr)  # IQR proximity rule: Min = q25 + 1,5 * IQR

    laps.loc[laps["LapTimeSeconds"] < laptime_min, "LapTimeSeconds"] = np.nan
    laps.loc[laps["LapTimeSeconds"] > laptime_max, "LapTimeSeconds"] = np.nan

    return laps


def getLaps(season, race):
    # Load the session data
    race = ff1.get_session(season, race, "R")

    # Get the laps
    race.load(laps=True, telemetry=True)
    laps = race.laps

    # Convert laptimes to seconds
    laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()

    return laps


def getLastRace():
    res = requests.get(f"https://ergast.com/api/f1/current/last.json")
    response = json.loads(res.text)
    season = response["MRData"]["RaceTable"]["season"]
    race = response["MRData"]["RaceTable"]["round"]
    raceName = response["MRData"]["RaceTable"]['Races'][0]['raceName']
    return int(season), int(race), raceName


def getTopFive(season, race):
    res = requests.get(f"https://ergast.com/api/f1/{season}/{race}/results.json")
    response = json.loads(res.text)
    topFive = []
    results = response['MRData']['RaceTable']['Races'][0]['Results']
    for pos in results:
        if int(pos['position']) <= 5:
            topFive.append(pos['Driver']['code'])
    return topFive


if __name__ == "__main__":
    makeRaceGraph()
