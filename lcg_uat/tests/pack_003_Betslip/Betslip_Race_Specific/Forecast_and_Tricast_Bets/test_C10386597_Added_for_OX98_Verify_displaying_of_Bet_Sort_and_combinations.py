import pytest
import tests
import voltron.environments.constants as vec
from random import choice
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C10386597_Added_for_OX98_Verify_displaying_of_Bet_Sort_and_combinations(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C10386597
    NAME: [Added for OX98] Verify displaying of Bet Sort and combinations
    DESCRIPTION: This test case verifies displaying of Bet Sort and combinations for Forecast/Tricast in Betslip
    PRECONDITIONS: Load app and login with user
    PRECONDITIONS: Navigate to HR page and open any event
    PRECONDITIONS: Select the 'Forecast' tab
    PRECONDITIONS: Note: This test case should be run for HR and for Greyhounds
    """
    keep_browser_open = True
    expected_estimate_returns = 'N/A'

    def betslip_verification(self, expected_selection_name, expected_selection):
        self.site.open_betslip()
        betslip = self.get_betslip_content()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')

        stake_name, stake = list(singles_section.items())[0]

        for actual_selection in singles_section:
            self.assertIn(actual_selection.strip(), expected_selection_name,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                              f'"{expected_selection_name}"')

        self.assertTrue(stake, msg=f'Stake "{stake_name}" was not found')
        self.assertEqual(stake.market_name, expected_selection,
                         msg=f'Market name "{stake.market_name}" '
                             f'is not the same as expected "{expected_selection}"')
        self.assertIn(stake.event_name, self.event_name,
                      msg=f'Event name and time "{stake.event_name}" '
                          f'is not the same as expected "{self.event_name}"')

        self.assertTrue(stake.amount_form.has_amount_input(), msg='"Amount input" is not displayed')
        self.assertEqual(stake.est_returns, self.expected_estimate_returns,
                         msg=f'Actual estimate returns: "{stake.est_returns}" is not the same as expected estimate returns:"{self.expected_estimate_returns}"')
        self.assertTrue(betslip.total_stake, msg='"Total Stake" is not displayed')
        self.assertTrue(stake.remove_button, msg='"Remove button" is not displayed')
        self.assertTrue(betslip.bet_now_button.is_displayed(), msg='"Place bet button" is not displayed')

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
            events = [event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')]

            if not events:
                raise SiteServeException(f'Cannot find active Forecast/Tricast Racing events')

            event = choice(events)
            start_time_local = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                          ob_format_pattern=self.ob_format_pattern,
                                                          future_datetime_format=self.my_bets_event_future_time_format_pattern,
                                                          ss_data=True)
            self.__class__.event_name = f'{event["event"]["name"]} {start_time_local}'
            self.__class__.event_id = event['event']['id']
            self._logger.info(
                f'*** Found Horse Racing Forecast/Tricast event "{self.event_name}" with id "{self.event_id}"')
        else:
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=5,
                                                              forecast_available=True,
                                                              tricast_available=True)
            event_start_time = event_params.event_date_time
            start_time_local = self.convert_time_to_local(date_time_str=event_start_time)
            self.__class__.event_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time_local}'
            self.__class__.event_id = event_params.event_id
            self._logger.info(
                f'*** Created Horse Racing Forecast/Tricast event "{self.event_name}" with id "{self.event_id}"')

        self.site.login()
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')

        tabs = self.market_tabs.items_as_ordered_dict
        self.assertTrue(tabs, msg='No market tabs found')
        self.assertIn(vec.racing.RACING_EDP_FORECAST_MARKET_TAB, tabs,
                      msg=f'"{vec.racing.RACING_EDP_FORECAST_MARKET_TAB}" not found in the list of tabs {list(tabs.keys())}')
        self.assertIn(vec.racing.RACING_EDP_TRICAST_MARKET_TAB, tabs,
                      msg=f'"{vec.racing.RACING_EDP_TRICAST_MARKET_TAB}" not found in the list of tabs {list(tabs.keys())}')

    def test_001_select_two_selection_from_any_placetap_add_to_betslip_and_navigate_to_betslipverify_that_reverse_forecast2_bet_is_shown_in_betslip(self):
        """
        DESCRIPTION: Select two selection from **ANY** Place
        DESCRIPTION: Tap 'Add to Betslip' and navigate to Betslip
        DESCRIPTION: Verify that 'Reverse Forecast(2)' bet is shown in Betslip
        EXPECTED: Bet is shown under SINGLES with appropriate elements:
        EXPECTED: - Remove button
        EXPECTED: - 'Stake' field
        EXPECTED: - Runners information according to selected runners (NOTE: Numbers for runner's place is not shown)
        EXPECTED: e.g. :  HorseDan
        EXPECTED: HorseTed
        EXPECTED: - Bet Sort: **Reverse Forecast 2**
        EXPECTED: - **From OX99** Event name and time
        EXPECTED: - Total Stake information
        EXPECTED: - Total Est. Returns information is displayed as 0 (zero) (**From OX99** Coral: Estimated Returns; Ladbrokes: Potential Returns')
        EXPECTED: - 'Place Bet' button
        """
        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(forecast=True,
                                                                                          any_button=True)

        expected_selection = f'{vec.betslip.REVERSE_FORECAST} 2'
        self.betslip_verification(expected_selection_name, expected_selection)

    def test_002_navigate_back_to_forecast_tabselect_3_or_more_selections_from_any_placetap_add_to_betslip_and_navigate_to_betslipverify_that_combination_forecast_n_bet_is_shown_in_betslipnote_calculation_of_n_no_of_selections_x_next_lowest_number_eg_4_selections_picked_4_x_3__12(self):
        """
        DESCRIPTION: Navigate back to 'Forecast' tab
        DESCRIPTION: Select 3 or more selections from **ANY** Place
        DESCRIPTION: Tap 'Add to Betslip' and navigate to Betslip
        DESCRIPTION: Verify that 'Combination Forecast <N>' bet is shown in Betslip
        DESCRIPTION: Note: Calculation of N: No of selections x next lowest number eg 4 Selections picked 4 x 3 = 12
        EXPECTED: One more bet is shown under SINGLES with appropriate elements:
        EXPECTED: - Remove button
        EXPECTED: - 'Stake' field
        EXPECTED: - Runners information according to selected runners (NOTE: Numbers for runner's place is not shown)
        EXPECTED: e.g. :  HorseDan
        EXPECTED: HorseTed
        EXPECTED: HourseTest (Quantity of runners names equal to added 'ANY place' selections)
        EXPECTED: - Bet Sort: **Combination Forecast <N>**
        EXPECTED: - **From OX99** Event name and time
        EXPECTED: - Total Stake information
        EXPECTED: - Total Est. Returns information is displayed as 0 (zero) (**From OX99** Coral: Estimated Returns; Ladbrokes: Potential Returns')
        EXPECTED: - 'Place Bet' button
        """
        self.clear_betslip()
        selections_number = 4
        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(forecast=True,
                                                                                          any_button=True,
                                                                                          any_iteration_range=selections_number)
        expected_selection = f'{vec.betslip.COMBINATION_FORECAST} {(selections_number - 1) * selections_number}'
        self.betslip_verification(expected_selection_name, expected_selection)

    def test_003_navigate_to_tricast_tabselect_3_or_more_selections_from_any_placetap_add_to_betslip_and_navigate_to_betslipverify_that_combination_tricast_n_bet_is_shown_in_betslip(self):
        """
        DESCRIPTION: Navigate to 'Tricast' tab
        DESCRIPTION: Select 3 or more selections from **ANY** Place
        DESCRIPTION: Tap 'Add to Betslip' and navigate to Betslip
        DESCRIPTION: Verify that 'Combination Tricast <N>' bet is shown in Betslip
        EXPECTED: One more bet is shown under SINGLES with appropriate elements:
        EXPECTED: - Remove button
        EXPECTED: - 'Stake' field
        EXPECTED: - Runners information according to selected runners (NOTE: Numbers for runner's place is not shown)
        EXPECTED: e.g. :  HorseDan
        EXPECTED: HorseTed
        EXPECTED: HourseTest (Quantity of runners names equal to added 'ANY place' selections)
        EXPECTED: - Bet Sort: **Combination Tricast <N>**
        EXPECTED: - **From OX99** Event name and time
        EXPECTED: - Total Stake information
        EXPECTED: - Total Est. Returns information is displayed as 0 (zero) (**From OX99** Coral: Estimated Returns; Ladbrokes: Potential Returns')
        EXPECTED: - 'Place Bet' button
        """
        self.clear_betslip()
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        selections_number = 3
        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(tricast=True,
                                                                                          any_button=True,
                                                                                          any_iteration_range=selections_number)
        expected_selection = f'{vec.betslip.COMBINATION_TRICAST} {(selections_number - 1) * selections_number}'
        self.betslip_verification(expected_selection_name, expected_selection)
