import json
import requests

import fastf1 as ff1
from fastf1 import utils
from fastf1 import plotting

from matplotlib import pyplot as plt

from RacePace import getLastRace


def makeTelemtryGraph():
    # Enable the cache by providing the name of the cache folder
    ff1.Cache.enable_cache("cache")

    season, race, _ = getLastRace()

    qualy = ff1.get_session(season, race, "Q")
    qualy.load()

    driver_1, driver_2 = getBestDrivers(qualy)

    # @TODO: Refactor

    # Select the fastest lap
    fastest_driver_1 = qualy.laps.pick_driver(driver_1).pick_fastest()
    fastest_driver_2 = qualy.laps.pick_driver(driver_2).pick_fastest()

    # Retrieve the telemetry and add the distance column
    telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
    telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()

    # Make sure whe know the team name for coloring
    team_driver_1 = fastest_driver_1["Team"]
    team_driver_2 = fastest_driver_2["Team"]

    # Extract the delta time
    delta_time, ref_tel, _ = utils.delta_time(fastest_driver_1, fastest_driver_2)

    # Make plot a bit bigger
    plt.rcParams["figure.figsize"] = [10, 10]

    # Create subplots with different sizes
    fig, ax = plt.subplots(3, gridspec_kw={"height_ratios": [3, 2, 1]})

    # Set the plot title
    ax[0].title.set_text(
        f"Qualifying Comparison {qualy.event.EventName}\n{driver_1} VS {driver_2}"
    )

    # Speed trace
    ax[0].plot(
        telemetry_driver_1["Distance"],
        telemetry_driver_1["Speed"],
        label=driver_1,
        color=ff1.plotting.team_color(team_driver_1),
    )
    ax[0].plot(
        telemetry_driver_2["Distance"],
        telemetry_driver_2["Speed"],
        label=driver_2,
        color=ff1.plotting.team_color(team_driver_2),
    )
    ax[0].set(ylabel="Speed")
    ax[0].legend(loc="lower right")

    # Throttle trace
    ax[1].plot(
        telemetry_driver_1["Distance"],
        telemetry_driver_1["Throttle"],
        label=driver_1,
        color=ff1.plotting.team_color(team_driver_1),
    )
    ax[1].plot(
        telemetry_driver_2["Distance"],
        telemetry_driver_2["Throttle"],
        label=driver_2,
        color=ff1.plotting.team_color(team_driver_2),
    )
    ax[1].set(ylabel="Throttle")

    # Delta line
    ax[2].plot(ref_tel["Distance"], delta_time)
    ax[2].axhline(0)
    ax[2].set(ylabel=f"<-- {driver_1} | {driver_2} -->")

    ax[2].set(xlabel="Lap distance (m)")
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for a in ax.flat:
        a.label_outer()

    # Store figure
    path = "./images/QualyTelemetry.png"
    plt.savefig(path, dpi=300)
    print("Figure saved (QualyTelemetry.png)")
    return path


def getBestDrivers(qualy):
    res = requests.get(
        f"https://ergast.com/api/f1/{qualy.event.EventDate.year}/{qualy.event.RoundNumber}/qualifying/1.json"
    )
    response = json.loads(res.text)
    driver1 = response["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"][0]["Driver"]["code"]
    res = requests.get(
        f"https://ergast.com/api/f1/{qualy.event.EventDate.year}/{qualy.event.RoundNumber}/qualifying/2.json"
    )
    response = json.loads(res.text)
    driver2 = response["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"][0]["Driver"]["code"]
    return driver1, driver2


def makeTelemetryMsg():
    txt = "📈 Telemetry Comparison 📉"
    img = makeTelemtryGraph()
    return txt, [img]


if __name__ == "__main__":
    makeTelemtryGraph()
