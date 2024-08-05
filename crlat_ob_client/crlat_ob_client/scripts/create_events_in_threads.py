import math
import threading

from crlat_ob_client.openbet_config import OBConfig


BRAND = 'ladbrokes'
ENV = 'tst2'
NUMBER_OF_ITERATIONS = 1
MAX_NUMBER_OF_THREADS = 10
EVENTS = []


def ob():
    return OBConfig(env=ENV, brand=BRAND)


def add_autotest_premier_league_football_event():
    e = ob().add_autotest_premier_league_football_event(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_autotest_premier_league_football_outright_event():
    e = ob().add_autotest_premier_league_football_outright_event(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_football_event_enhanced_multiples():
    e = ob().add_football_event_enhanced_multiples(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_football_event_to_special_league():
    e = ob().add_football_event_to_special_league(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_football_event_to_spanish_la_liga():
    e = ob().add_football_event_to_spanish_la_liga(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_spain_la_liga_football_outright_event():
    e = ob().add_spain_la_liga_football_outright_event(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_football_event_to_england_championship():
    e = ob().add_football_event_to_england_championship(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_football_event_to_italy_serie_a():
    e = ob().add_football_event_to_italy_serie_a(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_football_event_to_uefa_champions_league():
    e = ob().add_football_event_to_uefa_champions_league(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_football_event_to_england_premier_league():
    e = ob().add_football_event_to_england_premier_league(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_england_premier_league_football_outright_event():
    e = ob().add_american_football_event_to_nfl(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_football_event_to_autotest_league2():
    e = ob().add_football_event_to_autotest_league2(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_your_call_specials():
    e = ob().add_your_call_specials(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_tennis_event_to_autotest_trophy():
    e = ob().add_tennis_event_to_autotest_trophy(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_UK_racing_event():
    e = ob().add_UK_racing_event(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_UK_greyhound_racing_event():
    e = ob().add_UK_greyhound_racing_event(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_international_racing_event():
    e = ob().add_international_racing_event(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_racing_your_call_specials_event():
    e = ob().add_racing_your_call_specials_event(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_volleyball_event_to_austrian_league():
    e = ob().add_volleyball_event_to_austrian_league(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_rugby_league_event_to_rugby_league_all_rugby_league():
    e = ob().add_rugby_league_event_to_rugby_league_all_rugby_league(wait_for_event=False)
    EVENTS.append(e.event_id)


def add_sport():
    targets = [
        add_autotest_premier_league_football_event,
        add_autotest_premier_league_football_outright_event,
        add_football_event_enhanced_multiples,
        add_football_event_to_special_league,
        add_football_event_to_spanish_la_liga,
        add_spain_la_liga_football_outright_event,
        add_football_event_to_england_championship,
        add_football_event_to_italy_serie_a,
        add_football_event_to_uefa_champions_league,
        add_football_event_to_england_premier_league,
        add_england_premier_league_football_outright_event,
        add_football_event_to_autotest_league2,
        add_your_call_specials,
        add_tennis_event_to_autotest_trophy,
        add_UK_racing_event,
        add_UK_greyhound_racing_event,
        add_international_racing_event,
        add_racing_your_call_specials_event,
        add_volleyball_event_to_austrian_league,
        add_rugby_league_event_to_rugby_league_all_rugby_league
    ]
    threads = []

    start, end = 0, MAX_NUMBER_OF_THREADS
    for _ in range(0, math.ceil(len(targets) / MAX_NUMBER_OF_THREADS)):
        targets_ = targets[start:end]
        for target in targets_:
            thread = threading.Thread(target=target)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        start += MAX_NUMBER_OF_THREADS
        end += MAX_NUMBER_OF_THREADS
        threads = []


for _ in range(NUMBER_OF_ITERATIONS):
    add_sport()

ob()._logger.info(f'\n*** Created {len(EVENTS)} events: {EVENTS}')
