import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl # can't trigger live updates on prod/hl
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.liveserv_updates
@pytest.mark.races
@pytest.mark.next_races
@pytest.mark.low
@vtest
class Test_C141199_Verify_displaying_of_suspended_selection_on_Race_Landing_page_Next_4_Races_when_it_is_added_to_the_betslip(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C141199
    NAME: Verify displaying of suspended selection on <Race> Landing page ('Next 4 Races') when it is added to the betslip
    DESCRIPTION: This test case verifies displaying of suspended selection on <Race> Landing page ('Next 4 Races') when it is added to the betslip
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: YYYYYYY - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: 'priceTypeCodes' = 'LP'
    PRECONDITIONS: 'priceTypeCodes' = 'LP, SP'
    PRECONDITIONS: Notice, Price updates on <Race> Landing Page is possible ONLY for 'Today' tab on 'Next 4 Races' module.
    PRECONDITIONS: For the rest tabs: 'Tomorrow' and 'Future' -> 'Next 4 Races' module is not displayed there.
    """
    keep_browser_open = True
    prices_LP = {0: '1/5', 1: '2/3'}
    prices_LP_SP = {0: '1/2', 1: '1/3'}
    expected_betslip_counter_value = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing event
        EXPECTED: Racing event created
        """
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle.get('nextRacesComponentEnabled'):
            self._logger.warning('*** "NextRacesToggle -> nextRacesComponentEnabled" component is disabled. Needs to be enabled')
            self.cms_config.set_next_races_toggle_component_status(next_races_component_status=True)
        self.setup_cms_next_races_number_of_events()

        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)

        event_params_LP = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=2,
                                                             time_to_start=5, sp=False, lp=True,
                                                             lp_prices=self.prices_LP)
        self.__class__.selection_name_lp, self.__class__.selection_id_lp = list(event_params_LP.selection_ids.items())[0]
        self.__class__.event_id_LP = event_params_LP.event_id
        event_off_time_LP = event_params_LP.event_off_time
        self.__class__.event_name_LP = f'{event_off_time_LP} {self.horseracing_autotest_uk_name_pattern}'.upper()

        event_params_LP_SP = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=2,
                                                                time_to_start=10, sp=True, lp=True,
                                                                lp_prices=self.prices_LP_SP)
        self.__class__.event_id_LP_SP = event_params_LP_SP.event_id
        event_off_time_LP_SP = event_params_LP_SP.event_off_time
        self.__class__.event_name_LP_SP = f'{event_off_time_LP_SP} {self.horseracing_autotest_uk_name_pattern}'.upper()
        self.__class__.selection_name_lp_sp, self.__class__.selection_id_lp_sp = list(event_params_LP_SP.selection_ids.items())[0]

    def test_001_click_tap_on_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Click/Tap on <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_002_find_events_in_the_next_4_races_no_matter_what_price_type_it_has(self, expected_event_name=None):
        """
        DESCRIPTION: Find events in the Next 4 Races (no matter what price type it has)
        EXPECTED: Events are shown in the 'Next 4 Races' module
        """
        event_name = expected_event_name if expected_event_name else self.event_name_LP
        event = self.get_event_from_next_races_module(event_name=event_name)
        self.__class__.outcomes = event.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'No outcomes found for event {event_name}')

    def test_003_clicktap_on_price_odds_button_and_check_its_displaying(self):
        """
        DESCRIPTION: Click/Tap on Price/Odds button and check it's displaying
        EXPECTED: Selected Price/Odds button is marked as added to Betslip (Becomes green)
        """
        self.__class__.first_runner_name, first_runner = list(self.outcomes.items())[0]
        first_runner.bet_button.click()
        if self.device_type != 'desktop':
            self.site.add_first_selection_from_quick_bet_to_betslip()

        self.assertTrue(first_runner.bet_button.is_selected(timeout=5),
                        msg=f'Bet button is not selected for "{self.first_runner_name}"')

    def test_004_verify_that_selection_is_added_to_bet_slip(self):
        """
        DESCRIPTION: Verify that selection is added to Bet Slip
        EXPECTED: Selection is present in Bet Slip and counter is increased on header
        """
        self.site.open_betslip()

        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

        singles_section = self.get_betslip_sections().Singles
        stake_names = list(singles_section.keys())
        self.assertIn(self.first_runner_name, stake_names,
                      msg=f'Selection is not:q present in Betslip. Expected: {self.first_runner_name} \n Actual: {stake_names}')
        self.site.close_betslip()

    def test_005_trigger_the_following_situation_for_selected_outcome_of_win_or_each_way_market_outcome_status_code__s(self, expected_selection_id=None):
        """
        DESCRIPTION: Trigger the following situation for selected outcome of 'Win or Each Way' market:
        DESCRIPTION: outcomeStatusCode = 'S'
        """
        selection_id = expected_selection_id if expected_selection_id else self.selection_id_lp
        self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=False)

    def test_006_verify_outcome_for_the_event(self, expected_event_name=None, expected_selection_name=None):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Price/Odds button for outcome is displayed immediately as greyed out and become disabled but still displaying the prices in case it is 'priceTypeCodes' = 'LP'
        EXPECTED: * Price/Odds button for outcome is displayed immediately as greyed out and become disabled but still displaying the SP in case it is 'priceTypeCodes' = 'SP'
        EXPECTED: * Price/Odds button is not marked as added to Betslip (is not green anymore)
        EXPECTED: * Suspended outcome disappears from the 'Next 4 Races' module after page reloading
        EXPECTED: * The list of outcomes is refreshed after page reloading
        """
        event_name = expected_event_name if expected_event_name else self.event_name_LP
        selection_name = expected_selection_name if expected_selection_name else self.selection_name_lp

        autotest_event = self.get_event_from_next_races_module(event_name=event_name)
        autotest_event.scroll_to()
        outcomes = autotest_event.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes were found in {event_name} event')
        self.__class__.outcome = outcomes.get(selection_name)
        self.assertTrue(self.outcome, msg=f'Outcome "{selection_name}" was not found')

        result = self.outcome.bet_button.is_enabled(expected_result=False, timeout=50)  # TODO VOL-1970
        self.assertFalse(result, msg=f'Bet button for {selection_name} outcome was not disabled.')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Horseracing')

        autotest_event = self.get_event_from_next_races_module(event_name)
        outcomes = autotest_event.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes were found in {event_name} event')
        autotest_event.scroll_to()
        self.assertIsNone(outcomes.get(selection_name),
                          msg=f'Suspended outcome {selection_name} did not disappear after page refresh')

    def test_007_trigger_the_following_situation_for_selected_outcome_of_win_or_each_way__market_outcome_status_code__a(self, expected_selection_id=None):
        """
        DESCRIPTION: Trigger the following situation for selected outcome of 'Win or Each Way' market:
        DESCRIPTION: outcomeStatusCode = 'A'
        """
        selection_id = expected_selection_id if expected_selection_id else self.selection_id_lp
        self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=True)

    def test_008_verify_event_and_its_outcomes(self, expected_event_name=None, expected_selection_name=None):
        """
        DESCRIPTION: Verify event and its outcomes
        EXPECTED: * Disappeared outcome will be shown on the 'Next 4 Races' module after page reloading
        EXPECTED: * Price/Odds button of this event is no more disabled, they become active
        EXPECTED: * Price/Odds button is marked as added to Betslip (Becomes green)
        """

        event_name = expected_event_name if expected_event_name else self.event_name_LP
        selection_name = expected_selection_name if expected_selection_name else self.selection_name_lp

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Horseracing')

        event = self.get_event_from_next_races_module(event_name=event_name)
        event.scroll_to()
        outcomes = event.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes found for event {event_name}')
        outcome = outcomes.get(selection_name)
        self.assertTrue(outcome, msg=f'Outcome {selection_name} did not appear after page refresh')

        result = outcome.bet_button.is_enabled(timeout=3)
        self.assertTrue(result, msg=f'Bet button for {selection_name} outcome was not enabled.')

    def test_009_repeat_steps_for_event_with_lp_sp_prices(self):
        """
        DESCRIPTION: Verify event with  LP and SP and its outcomes suspending
        """
        self.test_002_find_events_in_the_next_4_races_no_matter_what_price_type_it_has(expected_event_name=self.event_name_LP_SP)
        self.test_003_clicktap_on_price_odds_button_and_check_its_displaying()
        self.__class__.expected_betslip_counter_value = 2
        self.test_004_verify_that_selection_is_added_to_bet_slip()
        self.test_005_trigger_the_following_situation_for_selected_outcome_of_win_or_each_way_market_outcome_status_code__s(expected_selection_id=self.selection_id_lp_sp)
        self.test_006_verify_outcome_for_the_event(expected_event_name=self.event_name_LP_SP,
                                                   expected_selection_name=self.selection_name_lp_sp)
        self.test_007_trigger_the_following_situation_for_selected_outcome_of_win_or_each_way__market_outcome_status_code__a(expected_selection_id=self.selection_id_lp_sp)
        self.test_008_verify_event_and_its_outcomes(expected_event_name=self.event_name_LP_SP,
                                                    expected_selection_name=self.selection_name_lp_sp)
