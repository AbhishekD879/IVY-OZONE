import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


# @pytest.mark.tst2  # Datafabric not available for tst2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.races
@vtest
class Test_C60094840_Verify_generic_silk_is_removed_when_bespoke_is_provided(BaseRacing):
    """
    TR_ID: C60094840
    NAME: Verify generic silk is removed when bespoke is provided
    DESCRIPTION: This test case verifies generic silk is removed when bespoke silk is provided for all races(UK and International)
    PRECONDITIONS: 1.Generic silk should display for all the horses by default
    PRECONDITIONS: If bespoke silk present it should display, otherwise generic silk should present
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def test_001_login_to_the_application_and_navigate_to_horse_racing_from_header_sub_menuin_mobile_from_sports_ribbonor_in_play___horse_racing(
            self):
        """
        DESCRIPTION: Login to the application and navigate to horse racing from header sub menu(In mobile from sports ribbon)
        DESCRIPTION: or In play - Horse racing
        EXPECTED: Horse racing landing page - meetings tab should display
        EXPECTED: if user is navigate from in play tab in play horse racing events should display
        """
        self.site.login()
        self.site.wait_content_state('homepage')
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing', timeout=20)
        current_tab_name = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Default tab is "{current_tab_name}" not "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')

    def test_002_verify_generic_silk_is_showing_while_page_load(self):
        """
        DESCRIPTION: Verify generic silk is showing while page load
        EXPECTED: While page load generic silk should display
        """
        self.site.wait_splash_to_hide(timeout=60)
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict.get(
            self.uk_and_ire_type_name)
        sections.scroll_to()
        found_event = False
        meetings = sections.items_as_ordered_dict
        self.assertTrue(meetings,
                        msg=f'Failed to display any meetings for section_name "{vec.racing.UK_AND_IRE_TYPE_NAME}"')
        for meeting_name, meeting in meetings.items():
            events = meeting.items_as_ordered_dict
            self.assertTrue(events,
                            msg=f'Failed to display any event for section_name "{vec.racing.UK_AND_IRE_TYPE_NAME}"')
            for event_name, event in events.items():
                if 'race-resulted' not in event.get_attribute('class'):
                    event.click()
                    self.site.wait_content_state_changed()
                    found_event = True
                if found_event is True:
                    break
            if found_event is True:
                break

        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='No market tabs found on EDP')
        outcomes = None
        for market_name, market in market_tabs.items():
            if market_name in ['FORECAST', 'TRICAST', 'TOTEPOOL']:
                continue
            market.click()
            sleep(3)  # Wait for outcomes to load
            self.site.wait_splash_to_hide(3)
            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one event section with outcomes found')
            section_name, section = list(sections.items())[0]
            outcomes = section.items_as_ordered_dict
            self.assertTrue(outcomes, msg='No outcome was found in section: "%s"' % market_name)
            break
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

    def test_003_verify_if_bespoke_silk_present_it_should_display_otherwise_generic_silk_should_present(self):
        """
        DESCRIPTION: Verify If bespoke silk present it should display otherwise generic silk should present
        """
        # Covered in Step2

    def test_004_verify_generic_silk_is_not_shown_when_bespoke_is_displayed(self):
        """
        DESCRIPTION: Verify generic silk is not shown when bespoke is displayed
        EXPECTED: Since on page load we are showing generic silk and overriding with bespoke silk it should not display again
        EXPECTED: ![](index.php?/attachments/get/115417132)
        """
        # Covered in Step2
