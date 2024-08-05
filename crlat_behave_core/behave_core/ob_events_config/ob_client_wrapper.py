from crlat_ob_client.openbet_config import OBConfig


class OBClientWrapper(object):
    def __init__(self, env, brand):
        self.event_id = None
        self.event_name = None
        self.all_markets_ids = None
        self.event_params = None
        self.default_market_id = None
        self.event_sort_code = None
        self.market_template = None
        self.market_name = None
        self.event_date_time = None
        self.team1 = None
        self.team2 = None
        self.selection_ids = None
        self.__class__.backend_env = env
        self.__class__.brand = brand
        self._get_selection_id_list = []
        self._get_selection_name_list = []
        self.race_type_id = None
        self.race_event_id = None
        self.race_selection_ids = None

    backend_env = None
    brand = None
    __ob_config = None

    @classmethod
    def get_ob_config(cls):
        if not cls.__ob_config:
            cls.__ob_config = OBConfig(env=cls.backend_env, brand=cls.brand)
        return cls.__ob_config

    @property
    def ob_config(self):
        self.get_ob_config()
        return self.__ob_config

    @property
    def get_event_id(self):
        return self.event_id

    @property
    def get_event_name(self):
        return self.event_name

    @property
    def get_event_params(self):
        return self.event_params

    @property
    def get_event_sort_code(self):
        return self.event_sort_code

    @property
    def get_market_template(self):
        return self.market_template

    @property
    def get_market_name(self):
        return self.market_name

    @property
    def get_selection_name_and_id_dict(self):
        return dict(zip(self._get_selection_name_list, self._get_selection_id_list))

    def get_selection_ids(self, selections_dict):
        self._get_selection_id_list = []
        self._get_selection_name_list = []
        for selection_name, selection in list(selections_dict.items()):
            if isinstance(selection, str):
                self._get_selection_id_list.append(selection)
            elif isinstance(selection, list):
                self._get_selection_id_list.extend(selection)
            elif isinstance(selection, dict):
                self._get_selection_id_list.extend(list(selection.values()))
                self._get_selection_name_list.extend(list(selection.keys()))
        return self._get_selection_id_list

    def add_sport_events(self, event_type=None, is_live=True, is_upcoming=False,
                         markets=None, event_prefix=None, **kwargs):
        ob_method = getattr(self.ob_config, event_type)
        self.event_params = ob_method(
            markets=markets,
            is_live=is_live,
            is_upcoming=is_upcoming,
            wait_for_event=False,
            event_prefix=event_prefix,
            **kwargs
        )
        self.event_id = self.event_params.event_id
        self.all_markets_ids = self.event_params.all_markets_ids[self.event_id] if markets is not None else None
        self.default_market_id = self.event_params.default_market_id
        self.event_date_time = self.event_params.event_date_time
        self.team1, self.team2 = self.event_params.team1, self.event_params.team2
        self.event_name = f'{self.team1} v {self.team2}'
        self.market_name = self.ob_config.event.market_name
        self.market_template = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name
        self.selection_ids = self.get_selection_ids(selections_dict=self.event_params.selection_ids)
        return self.event_params

    def add_racing_events(self, event_type, number_of_runners=5, markets=None, cashout=True, ew_terms=None,
                          lp_prices=None, wait_for_event=True, is_tomorrow=False, is_live=False, **kwargs):
        ob_method = getattr(self.ob_config, event_type)
        self.event_params = ob_method(
            number_of_runners=number_of_runners,
            cashout=cashout,
            ew_terms=ew_terms,
            lp_prices=lp_prices,
            wait_for_event=wait_for_event,
            is_tomorrow=is_tomorrow,
            markets=markets,
            is_live=is_live,
            **kwargs
        )
        self.race_event_id, self.race_selection_ids = self.event_params.event_id, dict(self.event_params.selection_ids)
        self.race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id
        return self.event_params

    def add_enhanced_multiples(self, event_type, is_live=False, **kwargs):
        ob_method = getattr(self.ob_config, event_type)
        self.event_params = ob_method(is_live=is_live, **kwargs)
        self.event_id = self.event_params.event_id
        self.default_market_id = self.event_params.default_market_id
        self.event_date_time = self.event_params.event_date_time
        self.team1, self.team2 = self.event_params.team1, self.event_params.team2
        self.event_name = f'{self.event_params.team1} v {self.event_params.team2}'
        self.selection_ids = self.get_selection_ids(selections_dict=self.event_params.selection_ids)
        return self.event_params

    def undisplay_all_events(self, event_id=None):
        event_id = event_id if event_id else self.event_id
        self.ob_config.change_event_state(event_id)


if __name__ == '__main__':
    client = OBClientWrapper(env='tst2', brand='bma')
    markets = [
        ('over_under_second_half', {'cashout': True}),
    ]
    sport_event = client.add_sport_events(event_type='add_autotest_premier_league_football_outright_event',
                                          markets=markets,
                                          is_live=False,
                                          is_upcoming=False)
    race_event = client.add_racing_events(event_type='add_UK_racing_event',
                                          number_of_runners=2)
    print(race_event)
    print(client.race_event_id, dict(client.race_selection_ids), client.race_type_id)
