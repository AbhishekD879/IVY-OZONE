import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from random import choice
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C10375628_Added_for_OX98_Verify_displaying_Betslip_with_Forecast(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C10375628
    NAME: [Added for OX98] Verify displaying Betslip with Forecast
    DESCRIPTION: This test case verifies displaying Forecast in Betslip
    PRECONDITIONS: 1. Load app and login with user
    PRECONDITIONS: 2. Navigate to Horse Races/Greyhounds page and open any event
    PRECONDITIONS: 3. Select 'Forecast' tab
    PRECONDITIONS: 4. Select '1st' and '2nd' runners
    PRECONDITIONS: 5. Tap 'Add to Betslip' button
    PRECONDITIONS: NOTE: This test case should be run for Horse Races and for Greyhounds
    """
    keep_browser_open = True
    expected_estimate_returns = 'N/A'

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
            self.__class__.event_name = f'{event["event"]["name"]}'
            self.__class__.event_id = event['event']['id']
            self._logger.info(f'*** Found Horse Racing Forecast/Tricast event "{self.event_name}" with id "{self.event_id}"')
        else:
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=5,
                                                              forecast_available=True,
                                                              tricast_available=True)
            self.__class__.event_name = f"{event_params.event_off_time} {self.horseracing_autotest_uk_name_pattern}"
            self.__class__.event_id = event_params.event_id
            self._logger.info(f'*** Created Horse Racing Forecast/Tricast event "{self.event_name}" with id "{self.event_id}"')
        self.site.login()

    def test_001_navigate_to_win_or_each_way_tab_on_horse_race_grayhound_event_pageverify_that_appropriate_runners_which_where_selected_on_forecast_tab_are_not_selected(self):
        """
        DESCRIPTION: Navigate to 'Win or each way' tab on Horse Race/ Grayhound event page
        DESCRIPTION: Verify that appropriate runners which where selected on 'Forecast' tab are not selected
        EXPECTED: - Appropriate runners are not selected on 'Win or each way' tab (selections are not highlighted)
        EXPECTED: - Single bets for the respective selections are NOT automatically added to the Betslip
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        self.place_forecast_tricast_bet_from_event_details_page(forecast=True)

    def test_002_navigate_to_betslipverify_that_forecast_single_bet_is_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that Forecast Single bet is shown
        EXPECTED: Forecast bet is shown under SINGLES with appropriate elements:
        EXPECTED: - 'Remove' button
        EXPECTED: - 'Stake' field
        EXPECTED: - Bet selection (Runners) information according to selected runners.
        EXPECTED: e.g. : 1 HorseDan
        EXPECTED: 2 HorseTed
        EXPECTED: **From OX99**:
        EXPECTED: 1st HorseDan
        EXPECTED: 2nd HorseTed
        EXPECTED: - **From OX99** Event name and time
        EXPECTED: - Bet Sort: **Forecast**
        EXPECTED: - Total Stake information
        EXPECTED: - Total Est. Returns information displayed as 0 (zero) (**From OX99** Coral: Estimated Returns; Ladbrokes: Potential Returns')
        EXPECTED: - 'Place Bet' button
        EXPECTED: NOTE: No singles selections are added to Betslip - only Forecast is added to Betslip
        """
        self.site.open_betslip()
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" are not added to the betslip')
        self.__class__.stake_name, stake = list(selections.items())[0]
        self.enter_stake_amount(stake=(self.stake_name, stake))
        betslip = self.get_betslip_content()
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.ordered_collection.values())[0]
        self.assertEqual(stake.market_name, 'Forecast',
                         msg=f'Actual Market name "{stake.market_name}" is not the same as expected "{"Forecast"}"')
        self.assertEqual(stake.event_name, self.event_name,
                         msg=f'Actual Event name "{stake.event_name}" is not the same as expected "{self.event_name}"')
        self.assertTrue(stake.amount_form.has_amount_input(), msg='"Amount input" is not displayed')
        self.assertEqual(stake.est_returns, self.expected_estimate_returns,
                         msg=f'Actual estimate returns: "{stake.est_returns}" is not the same as expected estimate returns:"{self.expected_estimate_returns}"')
        self.assertTrue(betslip.total_stake, msg='"Total Stake" is not displayed')
        self.assertTrue(stake.remove_button, msg='"Remove button" is not displayed')
        self.assertTrue(betslip.bet_now_button.is_displayed(), msg='"Place bet button" is not displayed')

    def test_003_add_a_stakeverify_that_total_est_returns_is_displayed_na(self):
        """
        DESCRIPTION: Add a Stake
        DESCRIPTION: Verify that Total Est. Returns is displayed N/A
        EXPECTED: - The stake is added and shown in the 'Stake' and 'Total Stake' fields
        EXPECTED: - Total Est. Returns information displayed as N/A (**From OX99** Coral: Estimated Returns; Ladbrokes: Potential Returns')
        """
        # Covered in step 2

    def test_004_add_a_selection_from_win_or_each_way_tab_on_horse_racegrayhound_edpverify_that_additional_single_selection_is_shown_in_betslip(self):
        """
        DESCRIPTION: Add a selection from 'Win or each way' tab on Horse race/Grayhound EDP
        DESCRIPTION: Verify that additional single selection is shown in Betslip
        EXPECTED: The Betslip is shown with 2 SINGLE selections:
        EXPECTED: - Forecast
        EXPECTED: - Single HR/Grayhound selection (e.g. Win or Each Way)
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        tab_name = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='No market tabs found')
        self.assertIn(tab_name, market_tabs.keys(),
                      msg=f'"{tab_name}" tab was not found in the tabs list "{market_tabs.keys()}"')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            tab_name)
        event_markets_list = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(event_markets_list, msg='No event market tabs found')
        event_market = event_markets_list[tab_name]
        outcomes = event_market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found')
        outcome = list(outcomes.values())[0]
        outcome.bet_button.click()
        self.site.open_betslip()
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" are not added to the betslip')
        stake1 = list(selections.values())[0]
        stake2 = list(selections.values())[1]
        self.assertEqual(stake1.market_name, 'Forecast',
                         msg=f'Actual Market name "{stake2.market_name}" is not the same as expected "{"Forecast"}"')
        self.assertEqual(stake2.market_name, 'Win or Each Way',
                         msg=f'Actual Market name "{stake2.market_name}" is not the same as expected "{"Win or Each Way"}"')
