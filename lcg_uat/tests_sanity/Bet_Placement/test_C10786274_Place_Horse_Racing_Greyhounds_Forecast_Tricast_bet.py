from random import choice

import pytest
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.event_details
@pytest.mark.horseracing
@pytest.mark.my_bets
@pytest.mark.open_bets
@pytest.mark.forecast_tricast
@pytest.mark.login
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@vtest
class Test_C10786274_Place_Horse_Racing_Greyhounds_Forecast_Tricast_bet(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C10786274
    NAME: Place Horse Racing/Greyhounds Forecast/Tricast bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Forecast/Tricast Bet on Horse Racing/Greyhounds
    PRECONDITIONS: Forecast and Tricast checkboxes are checked in TI for Horse Racing/Greyhound event (**Event1**)
    PRECONDITIONS: Login to application with positive balance user
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event and login
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.horseracing_config.category_id
            class_ids = self.get_class_ids_for_category(category_id=category_id)

            events_filter = self.ss_query_builder \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(
                    LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'SF,CF,RF,'))) \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(
                    LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CT,TC,'))) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE))

            ss_req = SiteServeRequests(env=tests.settings.backend_env, class_id=class_ids, brand=self.brand)
            resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
            events = [event for event in resp if event.get('event') and event['event'] and event['event'].get('children')]

            if not events:
                raise SiteServeException(f'Cannot find active Forecast/Tricast Racing events')

            event = choice(events)
            start_time_local = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                          ob_format_pattern=self.ob_format_pattern,
                                                          future_datetime_format=self.my_bets_event_future_time_format_pattern,
                                                          ss_data=True)
            self.__class__.event_name = f'{event["event"]["name"]} {start_time_local}'
            self.__class__.event_id = event['event']['id']
            self._logger.info(f'*** Found Horse Racing Forecast/Tricast event "{self.event_name}" with id "{self.event_id}"')
        else:
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=5,
                                                              forecast_available=True,
                                                              tricast_available=True)
            event_start_time = event_params.event_date_time
            start_time_local = self.convert_time_to_local(date_time_str=event_start_time)
            self.__class__.event_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time_local}'
            self.__class__.event_id = event_params.event_id
            self._logger.info(f'*** Created Horse Racing Forecast/Tricast event "{self.event_name}" with id "{self.event_id}"')

        self.site.login()

    def test_001_on_racing_edp_verify_that_forecast_tricast_tabs_are_shown(self):
        """
        DESCRIPTION: Navigate to Horse Racing Page
        DESCRIPTION: Open**Event1**Horse Racing/Greyhounds event
        DESCRIPTION: Verify that Forecast/Tricast tabs are shown
        EXPECTED: Forecast/Tricast tabs are shown Horse Racing/Greyhounds event
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')

        tabs = self.market_tabs.items_as_ordered_dict
        self.assertTrue(tabs, msg='No market tabs found')
        self.assertIn(vec.racing.RACING_EDP_FORECAST_MARKET_TAB, tabs,
                      msg=f'"{vec.racing.RACING_EDP_FORECAST_MARKET_TAB}" not found in the list of tabs {list(tabs.keys())}')
        self.assertIn(vec.racing.RACING_EDP_TRICAST_MARKET_TAB, tabs,
                      msg=f'"{vec.racing.RACING_EDP_TRICAST_MARKET_TAB}" not found in the list of tabs {list(tabs.keys())}')

    def test_002_on_forecast_tab_select_1st_and_2nd_runner_and_add_to_betslip_and_verify_that_forecast_bet_is_added(self):
        """
        DESCRIPTION: Navigate to Forecast tab
        DESCRIPTION: Select 1st and 2nd runner and add to Betslip
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'Forecast' bet is added to Betslip
        EXPECTED: Single 'Forecast' bet is added to Betslip
        """
        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(forecast=True)

        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')

        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]

        for actual_selection in singles_section:
            self.assertIn(actual_selection.strip(), expected_selection_name,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                              f'"{expected_selection_name}"')

        self.assertTrue(self.stake, msg=f'Stake "{expected_selection_name}" was not found')
        self.assertEqual(self.stake.market_name, vec.betslip.FORECAST,
                         msg=f'Market name "{self.stake.market_name}" '
                             f'is not the same as expected "{vec.betslip.FORECAST}"')

    def test_003_add_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and click on 'Place Bet' button
        EXPECTED: - The bet is successfully placed
        EXPECTED: - Bet receipt is shown
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_004_click_on_done_button(self):
        """
        DESCRIPTION: Click on 'Done' button
        EXPECTED: The customer is redirected to the Horse Racing/Greyhounds event details page
        """
        self.site.bet_receipt.footer.done_button.click()
        if self.device_type == 'desktop':
            self.device.refresh_page()
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_005_select_two_any_runners_and_verify_that_reverse_forecast_2_bet_is_added_to_betslip(self):
        """
        DESCRIPTION: Select two 'ANY' runners
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'Reverse Forecast 2' bet is added to Betslip
        EXPECTED: Single 'Reverse Forecast 2' bet is added to Betslip
        """
        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(forecast=True, any_button=True)

        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')

        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]

        for actual_selection in singles_section:
            self.assertIn(actual_selection.strip(), expected_selection_name,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                              f'"{expected_selection_name}"')

        self.assertTrue(self.stake, msg=f'Stake "{expected_selection_name}" was not found')
        self.assertEqual(self.stake.market_name, f'{vec.betslip.REVERSE_FORECAST} 2',
                         msg=f'Market name "{self.stake.market_name}" '
                             f'is not the same as expected "{vec.betslip.REVERSE_FORECAST} 2"')

    def test_006_add_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and click on 'Place Bet' button
        EXPECTED: - The bet is successfully placed
        EXPECTED: - Bet receipt is shown
        """
        self.test_003_add_stake_and_click_on_place_bet_button()

    def test_007_click_on_done_button(self):
        """
        DESCRIPTION: Click on 'Done' button
        EXPECTED: The customer is redirected to the Horse Racing/Greyhounds event details page
        """
        self.test_004_click_on_done_button()

    def test_008_select_more_than_two_any_runners_and_verify_that_combination_forecast_n_bet_is_added_to_betslip(self):
        """
        DESCRIPTION: Select more than two 'ANY' runners
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'Combination Forecast N' bet is added to Betslip
        EXPECTED: Single 'Combination Forecast N' bet is added to Betslip
        EXPECTED: where N is No of selections x next lowest number eg 4 Selections picked 4 x 3 = 12
        """
        selections_number = 4
        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(forecast=True, any_button=True,
                                                                                          any_iteration_range=selections_number)
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')

        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]

        expected_selection = f'{vec.betslip.COMBINATION_FORECAST} {(selections_number - 1) * selections_number}'
        for actual_selection in singles_section:
            self.assertIn(actual_selection.strip(), expected_selection_name,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                              f'"{expected_selection_name}"')

        self.assertTrue(self.stake, msg=f'Stake "{expected_selection_name}" was not found')
        self.assertEqual(self.stake.market_name, expected_selection,
                         msg=f'Market name "{self.stake.market_name}" '
                             f'is not the same as expected "{expected_selection}"')

    def test_009_add_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and click on 'Place Bet' button
        EXPECTED: - The bet is successfully placed
        EXPECTED: - Bet receipt is shown
        """
        self.test_003_add_stake_and_click_on_place_bet_button()

    def test_010_click_on_done_button(self):
        """
        DESCRIPTION: Click on 'Done' button
        EXPECTED: The customer is redirected to the Horse Racing/Greyhounds event details page
        """
        self.test_004_click_on_done_button()

    def test_011_click_on_my_bets_open_bets_verify_that_placed_bets_are_shown(self):
        """
        DESCRIPTION: Click on My Bets button from the header -> Select 'Open Bets'
        DESCRIPTION: Verify that placed bets are shown
        EXPECTED: Forecast, Reverse Forecast and Combination Forecast bets are shown
        """
        self.site.open_my_bets_open_bets()
        bet = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.keys())[0]
        self.assertTrue(bet, msg=f'{vec.bet_history.SINGLE_COMBINATION_FORECAST_MY_BETS_NAME} bet was not found')
        bet = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.keys())[1]
        self.assertTrue(bet, msg=f'{vec.bet_history.SINGLE_REVERSE_FORECAST_MY_BETS_NAME} bet was not found')
        bet = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.keys())[2]
        self.assertTrue(bet, msg=f'{vec.bet_history.SINGLE_FORECAST_MY_BETS_NAME} bet was not found')

    def test_012_on_tricast_tab_select_1st_2nd_and_3rd_runner_and_add_to_betslip_and_verify_that_tricast_bet_is_added(self):
        """
        DESCRIPTION: Navigate to Horse Racing Page from the Menu
        DESCRIPTION: Open**Event1**Horse Racing/Greyhounds event
        DESCRIPTION: Navigate to Tricast tab
        DESCRIPTION: Select 1st, 2nd, and 3rd runner and add to Betslip
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'Tricast' bet is added to Betslip
        EXPECTED: Single 'Tricast' bet is added to Betslip
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')

        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(tricast=True)

        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')

        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]

        for actual_selection in singles_section:
            self.assertIn(actual_selection.strip(), expected_selection_name,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                              f'"{expected_selection_name}"')

        self.assertTrue(self.stake, msg=f'Stake "{expected_selection_name}" was not found')
        self.assertEqual(self.stake.market_name, vec.betslip.TRICAST,
                         msg=f'Market name "{self.stake.market_name}" '
                             f'is not the same as expected "{vec.betslip.TRICAST}"')

    def test_013_add_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and click on 'Place Bet' button
        EXPECTED: - The bet is successfully placed
        EXPECTED: - Bet receipt is shown
        """
        self.test_003_add_stake_and_click_on_place_bet_button()

    def test_014_click_on_done_button(self):
        """
        DESCRIPTION: Click on 'Done' button
        EXPECTED: The customer is redirected to the Horse Racing/Greyhounds event details page
        """
        self.test_004_click_on_done_button()

    def test_015_select_three_or_more_any_runners_and_verify_that_combination_tricast_n_bet_is_added_to_betslip(self):
        """
        DESCRIPTION: Select three or more 'ANY' runners
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'Combination Tricast N' bet is added to Betslip
        EXPECTED: Single 'Combination Tricast N' bet is added to Betslip
        EXPECTED: where N is No of selections x next two lowest numbers
        EXPECTED: eg 4 Selections picked 4 x 3 x 2 = 24
        EXPECTED: 5 Selections picked 5 x 4 x 3 = 60 etc.
        """
        selections_number = 4
        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(tricast=True, any_button=True,
                                                                                          any_iteration_range=selections_number)
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')

        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]

        expected_selection = f'{vec.betslip.COMBINATION_TRICAST} {(selections_number - 2) * (selections_number - 1) * selections_number}'
        for actual_selection in singles_section:
            self.assertIn(actual_selection.strip(), expected_selection_name,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                              f'"{expected_selection_name}"')

        self.assertTrue(self.stake, msg=f'Stake "{expected_selection_name}" was not found')
        self.assertEqual(self.stake.market_name, expected_selection,
                         msg=f'Market name "{self.stake.market_name}" '
                             f'is not the same as expected "{expected_selection}"')

    def test_016_add_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and click on 'Place Bet' button
        EXPECTED: - The bet is successfully placed
        EXPECTED: - Bet receipt is shown
        """
        self.test_003_add_stake_and_click_on_place_bet_button()

    def test_017_click_on_done_button(self):
        """
        DESCRIPTION: Click on 'Done' button
        EXPECTED: The customer is redirected to the Horse Racing/Greyhounds event details page
        """
        self.test_004_click_on_done_button()

    def test_018_click_on_my_bets_open_bets_and_verify_that_placed_bets_are_shown(self):
        """
        DESCRIPTION: Click on My Bets button from the header -> Select 'Open Bets'
        DESCRIPTION: Verify that placed bets are shown
        EXPECTED: Tricast and Combination Tricast bets are shown
        """
        self.site.open_my_bets_open_bets()
        bet = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.keys())[0]
        self.assertTrue(bet, msg=f'{vec.bet_history.SINGLE_COMBINATION_TRICAST_MY_BETS_NAME} bet was not found')
        bet = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.keys())[1]
        self.assertTrue(bet, msg=f'{vec.bet_history.SINGLE_TRICAST_MY_BETS_NAME} bet was not found')
