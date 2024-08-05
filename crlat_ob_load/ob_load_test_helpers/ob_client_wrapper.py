import random

from ob_load_test_helpers.BaseMethods import BaseMethods
from ob_load_test_helpers.data import *
from ob_load_test_helpers.events_file_handler import *


class OBClientWrapper(object):
    def __init__(self, env, brand):
        if not self.base:
            self.__class__.base = BaseMethods(env=env, brand=brand)

    base = None
    event_with_selection_ids = {}

    def get_selection_ids(self, selections_dict):
        selection_ids = []
        for selection_name, selection in list(selections_dict.items()):
            if isinstance(selection, str):
                selection_ids.append(selection)
            elif isinstance(selection, list):
                selection_ids.extend(selection)
            elif isinstance(selection, dict):
                selection_ids.extend(list(selection.values()))
        return selection_ids

    def add_event(self, event_type, is_live=True, is_upcoming=False, markets=None, event_prefix=None,
                  **kwargs):
        ob_method = getattr(self.base.ob_config, event_type)
        event_params = ob_method(
            markets=markets,
            is_live=is_live,
            is_upcoming=is_upcoming,
            wait_for_event=False,
            team1=self.base.team1,
            team2=self.base.team2,
            event_prefix=event_prefix,
            **kwargs
        )
        selection_ids = self.get_selection_ids(selections_dict=event_params.selection_ids)
        self.__class__.event_with_selection_ids.update({event_params.event_id: selection_ids})

    def add_events(self, num_of_events=1, is_live=True, is_upcoming=False, markets=None, event_prefix=None,
                   add_extended_markets=False, **kwargs):
        markets = markets + extended_markets if add_extended_markets else markets
        events_key = 'live' if is_live else 'upcoming'
        try:
            for num in range(num_of_events):
                event_type = get_next_event_type()
                if 'football' in event_type and 'american' not in event_type and 'outright' not in event_type:
                    self.add_event(event_type=event_type, num_of_events=num_of_events,
                                   is_live=is_live, is_upcoming=is_upcoming, markets=markets,
                                   event_prefix=event_prefix, kwargs=kwargs)
                else:
                    self.add_event(event_type=event_type, num_of_events=num_of_events,
                                   is_live=is_live, is_upcoming=is_upcoming, markets=None,
                                   event_prefix=event_prefix, kwargs=kwargs)
        finally:
            write_events_ids_to_file({events_key: self.event_with_selection_ids})

    def get_random_selection(self, file_with_events, events_key='live', limit=None):
        events = read_events_ids_from_file(file_with_events)
        if 'both' in events_key:
            events_key = random.choice(list(events.keys()))
        selection_ids = random.choice(list(events[events_key].values()))
        if limit:
            return random.choice(list(reversed(selection_ids))[:limit])
        return random.choice(selection_ids)

    def update_random_event(self, file_with_events, events_key='live', limit=None):
        random_outcome = self.get_random_selection(file_with_events, events_key=events_key, limit=limit)
        new_price = str(round(random.uniform(1.0, 50.0), 2))
        self.base.ob_config.change_price(random_outcome, new_price)

    def change_random_selection_state(self, selection_id, active, displayed=True):
        self.base.ob_config.change_selection_state(selection_id=selection_id, displayed=displayed, active=active)

    def undisplay_all_events(self, file_with_events):
        events = read_events_ids_from_file(file_with_events)
        if 'live' in events:
            for event_id in list(events['live'].keys()):
                self.base.ob_config.change_event_state(event_id)
        if 'upcoming' in events:
            for event_id in list(events['upcoming'].keys()):
                self.base.ob_config.change_event_state(event_id)
