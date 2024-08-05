import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.medium
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@pytest.mark.portal_dependant
@vtest
class Test_C2554299_Format_of_PriceOdds_on_Open_Bets_and_Settled_Bets(BaseBetSlipTest):
    """
    TR_ID: C2554299
    NAME: Format of Price/Odds on 'Open Bets' and 'Settled Bets'
    DESCRIPTION: This test case verifies Price/Odds in decimal and fractional format on 'Open Bets' and 'Settled Bets'.
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed Singles and Multiple bets on events
    """
    keep_browser_open = True
    number_of_events = 2

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events and place bets
        """
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(number_of_events=self.number_of_events,
                                                         category_id=self.ob_config.football_config.category_id)
            # event 1
            local_start_time = self.convert_time_to_local(date_time_str=events[0]['event']['startTime'],
                                                          ob_format_pattern=self.ob_format_pattern,
                                                          ss_data=True,
                                                          future_datetime_format=self.event_card_future_time_format_pattern)
            self.__class__.event_name_1 = f'{normalize_name(events[0]["event"]["name"])} {local_start_time}'
            match_result_market = next((market['market'] for market in events[0]['event']['children'] if
                                        market.get('market').get('marketMeaningMinorCode') == 'MR' and
                                        market['market'].get('children')), None)
            outcomes = match_result_market['children']
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id_1 = list(selection_ids.values())[0]

            # event 2
            self.__class__.eventID_2 = events[1]['event']['id']
            local_start_time = self.convert_time_to_local(date_time_str=events[1]['event']['startTime'],
                                                          ob_format_pattern=self.ob_format_pattern,
                                                          ss_data=True,
                                                          future_datetime_format=self.event_card_future_time_format_pattern)
            self.__class__.event_name_2 = f'{normalize_name(events[1]["event"]["name"])} {local_start_time}'
            match_result_market2 = next((market['market'] for market in events[1]['event']['children'] if
                                         market.get('market').get('marketMeaningMinorCode') == 'MR' and
                                         market['market'].get('children')), None)
            outcomes_2 = match_result_market2['children']

            selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_2}
            selection_id_2 = list(selection_ids2.values())[0]

        else:
            event_params_1 = self.ob_config.add_autotest_premier_league_football_event()
            selection_id_1 = event_params_1.selection_ids[event_params_1.team1]

            local_start_time = self.convert_time_to_local(date_time_str=event_params_1.event_date_time)
            self.__class__.event_name_1 = f'{event_params_1.team1} v {event_params_1.team2} {local_start_time}'

            event_params_2 = self.ob_config.add_autotest_premier_league_football_event()
            selection_id_2 = event_params_2.selection_ids[event_params_2.team2]

            local_start_time = self.convert_time_to_local(date_time_str=event_params_2.event_date_time)
            self.__class__.event_name_2 = f'{event_params_2.team1} v {event_params_2.team2} {local_start_time}'

        self.site.login(username=tests.settings.betplacement_user)

        self.open_betslip_with_selections(selection_ids=selection_id_1)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        self.__class__.expected_betslip_counter_value = 0

        self.open_betslip_with_selections(selection_ids=(selection_id_1, selection_id_2))
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

    def test_001_navigate_to_open_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab on 'My Bets' page
        """
        self.navigate_to_page(name='open-bets')
        self.site.wait_content_state('OpenBets')

    def test_002_verify_priceodds_of_single_selection(self):
        """
        DESCRIPTION: Verify Price/Odds of Single selection
        EXPECTED: Format of Price/Odds corresponds to: 'priceNum'/'priceDen' attributes (i.e.9/1)
        """
        if not self.is_mobile:
            self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=self.event_name_1, bet_type='SINGLE', number_of_bets=2)

        self.assertTrue(bet.items_as_ordered_dict.items(), msg='No betlegs found')

        for betleg_name, betleg in bet.items_as_ordered_dict.items():
            self.assertRegexpMatches(betleg.odds_value, self.fractional_pattern,
                                     msg=f'Stake odds of {betleg_name} bet does not match fractional pattern')

    def test_003_verify_priceodds_of_multiples_selection(self):
        """
        DESCRIPTION: Verify Price/Odds of Multiples selection
        EXPECTED: Fractional format Price/Odds correspons to: 'priceNum'/'priceDen' attributes (i.e.9/1)
        """
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=[self.event_name_1, self.event_name_2], bet_type='DOUBLE', number_of_bets=2)

        self.assertTrue(bet.items_as_ordered_dict.items(), msg='No betlegs found')

        for betleg_name, betleg in bet.items_as_ordered_dict.items():
            self.assertRegexpMatches(betleg.odds_value, self.fractional_pattern,
                                     msg=f'Stake odds of {betleg_name} bet does not match fractional pattern')

    def test_004_switch_to_decimal_format_for_the_user(self):
        """
        DESCRIPTION: Switch to Decimal format for the user
        """
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(result, msg=f'Odds format is not changed to "{vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC}"')

    def test_005_navigate_to_open_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab on 'My Bets' page
        """
        self.navigate_to_page(name='open-bets')
        self.site.wait_content_state('OpenBets')

    def test_006_verify_priceodds_of_single_selection(self):
        """
        DESCRIPTION: Verify Price/Odds of Single selection
        EXPECTED: Format of Price/Odds corresponds to: 'priceDec' atribute (i.e.10)
        """
        if not self.is_mobile:
            self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=self.event_name_1, bet_type='SINGLE', number_of_bets=2)

        self.assertTrue(bet.items_as_ordered_dict.items(), msg='No betlegs found')

        for betleg_name, betleg in bet.items_as_ordered_dict.items():
            self.assertRegexpMatches(betleg.odds_value, self.decimal_pattern,
                                     msg=f'Stake odds of {betleg_name} bet does not match decimal pattern')

    def test_007_verify_priceodds_of_multiples_selection(self):
        """
        DESCRIPTION: Verify Price/Odds of Multiples selection
        EXPECTED: Format of Price/Odds corresponds to: 'priceDec' atribute (i.e.10)
        """
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=[self.event_name_1, self.event_name_2], bet_type='DOUBLE', number_of_bets=2)

        self.assertTrue(bet.items_as_ordered_dict.items(), msg='No betlegs found')

        for betleg_name, betleg in bet.items_as_ordered_dict.items():
            self.assertRegexpMatches(betleg.odds_value, self.decimal_pattern,
                                     msg=f'Stake odds of {betleg_name} bet does not match decimal pattern')
