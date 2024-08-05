import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from time import sleep


@pytest.mark.desktop
@pytest.mark.prod
# @pytest.mark.tst2  # Datafabric not available for tst2
# @pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.horseracing
@vtest
class Test_C60094836_Verify_page_load_time_when_bespoke_silks_are_provided(BaseRacing):
    """
    TR_ID: C60094836
    NAME: Verify page load time when bespoke silks are provided
    DESCRIPTION: This test case verifies page load time is not impacted when bespoke silk is provided for all races(UK and International)
    DESCRIPTION: Since each generic silk is overriding with bespoke silk performance should not impact
    PRECONDITIONS: 1.Generic silk should display for all the horses by default
    PRECONDITIONS: If bespoke silk present it should display otherwise generic silk should present
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def test_001_login_to_the_application_and_navigate_to_horse_racing_from_header_sub_menuin_mobile_from_sports_ribbonor_in_play___horse_racing(self):
        """
        DESCRIPTION: Login to the application and navigate to horse racing from header sub menu(In mobile from sports ribbon)
        DESCRIPTION: or In play - Horse racing
        EXPECTED: Horse racing landing page - meetings tab should display
        EXPECTED: if user is navigate from in play tab in play horse racing events should display
        """
        self.site.login()
        self.site.wait_content_state(state_name='homepage')
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn('HORSE RACING', sports.keys(), msg=f'"{vec.racing.HORSE_RACING_TAB_NAME}" is not found in the header sport menu')
            sports.get('HORSE RACING').click()
        else:
            self.navigate_to_page('horse-racing')
        self.site.wait_content_state(state_name='Horseracing')
        current_tab_name = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab "{current_tab_name}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')

    def test_002_click_on_hr_events_and_verify_page_load(self):
        """
        DESCRIPTION: Click on HR events and verify page load
        EXPECTED: Page load should not impact
        """
        self.site.wait_splash_to_hide()
        sleep(3)
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict.get(
            self.uk_and_ire_type_name)
        found_event = False
        meetings = sections.items_as_ordered_dict
        self.assertTrue(meetings, msg=f'Failed to display any meetings for section_name "{vec.racing.UK_AND_IRE_TYPE_NAME}"')
        for meeting_name, meeting in meetings.items():
            events = meeting.items_as_ordered_dict
            self.assertTrue(events, msg=f'Failed to display any event for section_name "{vec.racing.UK_AND_IRE_TYPE_NAME}"')
            for event_name, event in events.items():
                if 'race-on' in event.get_attribute('class'):
                    event.click()
                    self.site.wait_content_state_changed(10)
                    found_event = True
                if found_event is True:
                    break
            if found_event is True:
                    break

        if self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()

        current_market_tab = self.site.racing_event_details.tab_content.event_markets_list.current_market_tab_name
        if current_market_tab != vec.racing.RACING_EDP_MARKET_TABS.win_or_ew:
            market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
            if vec.racing.RACING_EDP_MARKET_TABS.win_or_ew in market_tabs.keys():
                market_tabs[vec.racing.RACING_EDP_MARKET_TABS.win_or_ew].click()
                self.site.wait_content_state_changed(timeout=5)

                if self.site.wait_for_my_stable_onboarding_overlay():
                    self.site.my_stable_onboarding_overlay.close_button.click()

        market_tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        selected_market = list(market_tab.values())[0]
        outcomes = selected_market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % selected_market)
        for outcome_name, outcome in list(outcomes.items()):
            self.assertTrue(outcome.horse_name, msg=f'Failed to display the horse name "{outcome.horse_name}" '
                            f'from section "{outcome_name}"')
            # Generic Silk
            if outcome.horse_name == 'Unnamed Favourite' or outcome.horse_name == 'Unnamed 2nd Favourite':
                self.assertTrue(outcome.has_silks,
                                msg=f'Silk is not displayed for the horse "{outcome.horse_name}" from section "{outcome_name}"')
            # No silk at all
            elif outcome.is_non_runner:
                self.assertTrue(outcome.has_no_silks,
                                msg=f'Silk is displayed for non-runner horse "{outcome.horse_name}" from section "{outcome_name}"')
            # Bespoke Silk
            elif outcome.silk:
                self.assertTrue(outcome.has_bespoke_silks,
                                msg=f'Bespoke silk is not displayed for the horse "{outcome.horse_name}" from section "{outcome_name}"')
            # Generic Silk
            else:
                self.assertTrue(outcome.is_silk_generic, msg=f'Silk icon is not generic for outcome: "{outcome_name}"')
