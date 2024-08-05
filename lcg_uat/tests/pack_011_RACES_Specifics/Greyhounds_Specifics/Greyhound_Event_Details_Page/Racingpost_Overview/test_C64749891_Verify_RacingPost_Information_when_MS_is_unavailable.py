import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.environments import constants as vec


# @pytest.mark.tst2 # Racing Post Info is not available
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.other
@pytest.mark.desktop
@vtest
class Test_C64749891_Verify_RacingPost_Information_when_MS_is_unavailable(BaseGreyhound):
    """
    TR_ID: C64749891
    NAME: Verify RacingPost Information when MS is unavailable
    DESCRIPTION: This testcase verifies RacingPost
    DESCRIPTION: Information when MS is unavailable
    PRECONDITIONS: User should have CMS access
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - Racingpost info should be displayed.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get Greyhound Race Event
        """
        racing_datahub_status = self.get_initial_data_system_configuration().get('RacingDataHub')[
            "isEnabledForGreyhound"]
        if not racing_datahub_status:
            self.cms_config.update_system_configuration_structure(config_item='RacingDataHub',
                                                                  field_name='isEnabledForGreyhound',
                                                                  field_value=True)
        self.__class__.event_id = self.get_event_details(racing_post_pick=True).event_id

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state('Homepage')

    def test_002_go_to_the_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to the Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing', timeout=20)

    def test_003_trigger_error_from_racingpost_ms_not_availablenot_responding(self):
        """
        DESCRIPTION: Trigger error from RacingPost MS (not available/not responding)
        EXPECTED: Error is received in response from RacingPost MS
        """
        # cannot automate

    def test_004_select_event_with_racingpost_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with RacingPost available and go to its details page
        EXPECTED: * Event details page is opened successfully
        EXPECTED: * No error is displayed on Event details page
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

    def test_005_verify_event_details_page(self):
        """
        DESCRIPTION: Verify Event details page
        EXPECTED: * Racingpost Overview is not loaded
        EXPECTED: * Markets are displayed according to SS response
        EXPECTED: * Each-way terms are displayed according to SS response (if available)
        """
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertIn(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB, markets,
                      msg=f'"{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB}" market is not in "{markets}" markets')
        w_or_ew_section = markets.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        ew_terms = w_or_ew_section.name
        self.assertTrue(ew_terms, msg='Each Way terms are empty')
        self.__class__.outcomes = w_or_ew_section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes found')

    def test_006_go_to_selection_level_and_tap_it(self):
        """
        DESCRIPTION: Go to selection level and tap it
        EXPECTED: * Racingpost Selection Overview is not loaded
        EXPECTED: * Selection name is displayed
        EXPECTED: * Runner number and silk are shown
        EXPECTED: * Odds are shown next to selection name
        """
        for outcome_name, outcome in self.outcomes.items():
            if 'Unnamed Favourite' not in outcome_name:
                self.assertTrue(outcome.has_silks, msg=f'Silk icon is not displayed for outcome: "{outcome_name}"')
                self.assertTrue(outcome.bet_button, msg=f'Bet Button is not displayed for outcome: "{outcome_name}"')
