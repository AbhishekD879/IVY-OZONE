import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound


# @pytest.mark.tst2 # Racing Post Info is not available
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.greyhounds
@pytest.mark.event_details
@vtest
class Test_C64749890_Verify_ShowMore_check_for_Win_EWTop_finishto_finish_etc_tabs_also(BaseGreyhound):
    """
    TR_ID: C64749890
    NAME: Verify ShowMore (check for Win /EW,Top finish,to finish etc tabs also)
    DESCRIPTION: This testcase verifies ShowMore
    DESCRIPTION: feature
    PRECONDITIONS: User should have CMS access
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - Racingpost info should be displayed.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get Greyhound Race Event
        """
        racing_datahub_status = self.get_initial_data_system_configuration().get('RacingDataHub')["isEnabledForGreyhound"]
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
        # Covered in below step

    def test_002_go_to_the_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to the Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        # Covered in below step

    def test_003_select_event_with_raingpost_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with RaingPost available and go to its details page
        EXPECTED: Event details page is opened
        EXPECTED: * 'Win or E/W' market is selected by default
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='greyhound-racing')
        markets_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list
        if markets_tabs.current != vec.racing.RACING_EDP_MARKET_TABS.win_or_ew:
            markets_tabs.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
            self.site.wait_content_state_changed(timeout=5)

    def test_004_go_to_selection_area_and_verify_for_the_description_of_the_eventverify_show_more_optionverify_show_less_option(self):
        """
        DESCRIPTION: Go to selection area and verify for the description of the event
        DESCRIPTION: *Verify 'Show More' option
        DESCRIPTION: *Verify 'Show Less' option
        EXPECTED: 4.'Show More' option is displayed
        EXPECTED: * 'Show More' option becomes 'Show Less' after tapping it
        EXPECTED: * All RacingPost Selection Summary is displayed after tapping 'Show More' option
        EXPECTED: * 'Show Less' option becomes 'Show More' after tapping it
        EXPECTED: * Part of RacingPost Selection Summary is collapsed after tapping 'Show Less' option
        """
        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]
        outcomes = market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='Market does not have any items')

        for outcome_name, outcome in list(outcomes.items())[:4] if len(
                outcomes) > 4 else outcomes.items():
            outcomes = market.items_as_ordered_dict
            outcome.scroll_to()
            if 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                self.assertTrue(outcome.has_show_summary_toggle(),
                                msg=f'Show more button is not present for "{outcome_name}"')
                if outcome.toggle_icon_name.lower() != vec.racing.SHOW_LESS.lower():
                    expected_button_name = 'Show More'
                    result = wait_for_result(
                        lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_MORE.lower(),
                        name=f'Button name {vec.racing.SHOW_MORE}',
                        timeout=1)
                    self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_MORE}" '
                                                f'is not same as expected "{expected_button_name}" for outcome: {outcome_name}')
                    outcome.show_summary_toggle.click()
                self.assertTrue(wait_for_result(lambda: outcome.has_expanded_summary(), timeout=5),
                                msg=f'Summary is not shown for outcome "{outcome_name}" after expanding selection')
                has_spotlight_info = outcome.expanded_summary.has_spotlight_info
                self.assertTrue(has_spotlight_info, msg="SPOTLIGHT info is not shown")

                expected_button_name = 'Show Less'
                result = wait_for_result(
                    lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_LESS.lower(),
                    name=f'Button name {vec.racing.SHOW_LESS}',
                    timeout=1)
                self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                            f'is the same as expected "{expected_button_name}"for outcome: {outcome_name}')

        for outcome_name, outcome in list(outcomes.items())[:4] if len(
                outcomes) > 4 else outcomes.items():
            outcomes = market.items_as_ordered_dict
            outcome.scroll_to()
            if 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                self.assertTrue(outcome.has_show_summary_toggle(),
                                msg=f'Show more button is not present for "{outcome_name}"')
                if outcome.toggle_icon_name.lower() != vec.racing.SHOW_MORE.lower():
                    expected_button_name = 'Show Less'
                    result = wait_for_result(
                        lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_LESS.lower(),
                        name=f'Button name {vec.racing.SHOW_LESS}',
                        timeout=1)
                    self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                                f'is not same as expected "{expected_button_name}" for outcome: {outcome_name}')
                    outcome.show_summary_toggle.click()
                self.assertFalse(
                    wait_for_result(lambda: outcome.has_expanded_summary(expected_result=False), timeout=5),
                    msg=f'Summary is shown for outcome "{outcome_name}" after expanding selection')
                expected_button_name = 'Show More'
                result = wait_for_result(
                    lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_MORE.lower(),
                    name=f'Button name {vec.racing.SHOW_MORE}',
                    timeout=1)
                self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_MORE}" '
                                            f'is the same as expected "{expected_button_name}"for outcome: {outcome_name}')

