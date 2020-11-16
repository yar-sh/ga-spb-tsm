from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from Station import Station
from Neighbour import Neighbour
from transliterate import translit
from static_data import *
from helpers import *
import time
import json
import itertools

URL = "https://yandex.ru/metro/saint-petersburg"
LINE_COLORS = ["rgb(218, 33, 40)", "rgb(0, 120, 191)", "rgb(72, 184, 94)", "rgb(245, 130, 32)", "rgb(142, 71, 155)"]

def gen_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-3d-apis")
    opts.add_argument("--disable-plugins")
    opts.add_argument("--disable-accelerated-video")
    opts.add_argument("--disable-translate")
    opts.add_argument("--incognito")
    opts.add_argument("--kiosk")
    opts.add_argument("--no-experiments")
    opts.add_argument("--no-pings")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=opts)
    driver.set_window_position(0, 0)
    driver.set_window_size(1366/2, 1200)

    return driver


def wait_until_ready(driver : webdriver.Chrome):
    while True:
        if driver.execute_script("return document.readyState === 'complete'"):
            time.sleep(1)
            return

        time.sleep(0.5)


def get_stations(driver : webdriver.Chrome) -> list:
    # In this JS statement we explicitly ignore Зенит station, since it is closed and we won't be able to visit it
    station_names = driver.execute_script("""
        return Array.from(document.getElementsByClassName("scheme-objects-view__label _hoverable")).map(x=> {
            let tspans = Array.from(x.getElementsByTagName("tspan"))
            return tspans.slice(0, tspans.length/2).map(x => x.textContent.charAt(0).toUpperCase() + x.textContent.slice(1)).join(" ");
        }).filter(x => x.indexOf("Зенит") === -1);
    """)

    stations = []

    for n in range(len(station_names)):
        s = Station()
        s.id = n + 1
        s.name = station_names[n]
        s.name_eng = translit(s.name, "ru", reversed=True)

        stations.append(s)

    return stations


def enter_first_station(driver: webdriver.Chrome, station: Station):
    el = driver.find_element_by_css_selector("body > div.metro-body > div > div.metro-app__sidebar-container > div.metro-sidebar-view > div > div > div.scroll__content > div.metro-input-form > div > div.metro-input-form__suggest-container > div.metro-input-form__stop-suggest._type_from > div.suggest > span > span > input")
    el.send_keys(Keys.CONTROL + "a")
    el.send_keys(Keys.DELETE)
    el.send_keys(station.name)
    el.send_keys(Keys.ENTER)
    time.sleep(0.2)


def enter_second_station(driver: webdriver.Chrome, station: Station):
    el = driver.find_element_by_css_selector("body > div.metro-body > div > div.metro-app__sidebar-container > div.metro-sidebar-view > div > div > div.scroll__content > div.metro-input-form > div > div.metro-input-form__suggest-container > div.metro-input-form__stop-suggest._type_to > div.suggest > span > span > input")
    el.send_keys(Keys.CONTROL + "a")
    el.send_keys(Keys.DELETE)
    el.send_keys(station.name)
    el.send_keys(Keys.ENTER)
    time.sleep(0.2)


def reset_route(driver : webdriver.Chrome):
    driver.find_element_by_css_selector("""body > div.metro-body > div > div.metro-app__sidebar-container > div.metro-sidebar-view > div > div > div.scroll__content > div.metro-input-form > div.metro-input-form__buttons > div""").click()
    time.sleep(0.1)


def get_line(driver: webdriver.Chrome):
    bg_color = driver.execute_script("""
        return document.getElementsByClassName("metro-input-form__stop-icon")[0].style.backgroundColor;
    """)

    return LINE_COLORS.index(bg_color) + 1


def get_travel_interval(driver: webdriver.Chrome):
    return driver.execute_script("""
        return Number(document.getElementsByClassName("route-metro-details-step-view__metro-minutes")[0].textContent.split(" ")[0]);
    """)


def get_travel_time(driver: webdriver.Chrome):
    return driver.execute_script("""
        return Number(document.getElementsByClassName("route-masstransit-step-view__details-info-left-content")[0].textContent.split(" ")[0]);
    """)


def gather_stations_info(driver:webdriver.Chrome, stations:list):
    # Populate line numbers, travel_interval, and travel_time
    for i in range(len(stations)):
        enter_first_station(driver, stations[i])

        stations[i].line = get_line(driver)

        # If this is a different line from the previous neighbour, then these stations cannot be neighbours
        if i > 0 and stations[i-1].line != stations[i].line:
            stations[i-1].neighbours = [n for n in stations[i-1].neighbours if n.station.id != stations[i].id]

        if i + 1 == len(stations):
            break

        enter_second_station(driver, stations[i+1])

        n = Neighbour()
        n.station = stations[i+1]
        n.travel_interval = get_travel_interval(driver)
        n.travel_time = get_travel_time(driver)
        stations[i].neighbours.append(n)

        print(stations[i])
        reset_route(driver)
        time.sleep(0.5)


def parse_transfers(driver:webdriver.Chrome, stations:list):
    # For each transfer point, we permute every 2 stations, so that we get
    #   all off the traveling times

    for transfer in TRANSFERS:
        for st_pair in list(itertools.permutations(transfer, 2)):
            st1 = stations[st_pair[0] - 1]
            st2 = stations[st_pair[1] - 1]

            enter_first_station(driver, st1)
            enter_second_station(driver, st2)

            n = Neighbour()
            n.station = st2
            n.travel_interval = 0
            n.travel_time = get_travel_time(driver)
            n.travel_method = "walk"

            st1.neighbours.append(n)

            reset_route(driver)
            time.sleep(0.5)


def parse_taxi(stations:list):
    for t in TAXI:
        n = Neighbour()
        n.station = stations[t["to"] - 1]
        n.travel_interval = t["travel_interval"]
        n.travel_time = t["travel_time"]
        n.travel_method = "taxi"

        stations[t["from"] - 1].neighbours.append(n)


if __name__ == "__main__":
    driver = gen_driver()
    driver.get(URL)
    wait_until_ready(driver)

    stations = get_stations(driver)

    gather_stations_info(driver, stations)
    stations.reverse()
    gather_stations_info(driver, stations)
    stations.reverse()

    #stations = load_stations_from_file()

    parse_transfers(driver, stations)
    parse_taxi(stations)

    dump_stations_to_file(stations)
    driver.close()
