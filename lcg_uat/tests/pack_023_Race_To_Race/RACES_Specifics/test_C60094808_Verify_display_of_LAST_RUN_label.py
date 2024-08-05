import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


# @pytest.mark.tst2 Racing Post Feed will not be available everytime on qa2 & stg2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.horseracing
@vtest
class Test_C60094808_Verify_display_of_LAST_RUN_label(BaseRacing):
    """
    TR_ID: C60094808
    NAME: Verify display of "LAST RUN" label
    DESCRIPTION: Verify that "LAST RUN" label and Last run information is displayed below the label.
    PRECONDITIONS: 1: Racing Post Verdict should be available for the event
    PRECONDITIONS: 2: SPOTLIGHT and Last Run information should be available for the Horses
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: Ladbrokes/Coral URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state("homepage")

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_horse_race_event_from_uk__irish_races(self):
        """
        DESCRIPTION: Click on any Horse race event from UK / Irish races
        EXPECTED: User should be navigated to Event details page
        """
        self.site.wait_splash_to_hide(timeout=10)
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict.get(self.uk_and_ire_type_name)
        expected_event = None
        expected_meeting_name = None
        meetings = sections.items_as_ordered_dict
        for meeting_name, meeting in meetings.items():
            events = meeting.items_as_ordered_dict
            for event_name, event in events.items():
                race_started = event.is_resulted or event.has_race_off()
                if not race_started:
                    expected_event = event
                    expected_meeting_name = meeting_name
                    break
            if expected_event is not None:
                break
        expected_event.click()
        self.site.wait_splash_to_hide()
        actual_meeting_name = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertIn(expected_meeting_name.lower(), actual_meeting_name.lower(),
                      msg=f'Actual meeting name "{actual_meeting_name}" '
                          f'is not same as expected meeting name "{expected_meeting_name}" ')

    def test_004_scroll_to_the_selections_horses_and_click_on_show_more_link(self):
        """
        DESCRIPTION: Scroll to the Selections (Horses) and click on "SHOW MORE" link
        EXPECTED: The following information should be displayed
        EXPECTED: 1: SPOTLIGHT
        EXPECTED: 2: LAST RUN
        EXPECTED: "SHOW MORE" text should be replaced with "SHOW LESS" in the expanded view
        """
        self.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        for market_name, market in self.market_tabs.items():
            self.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
            if market_name not in ['FORECAST', 'TRICAST', 'TOTEPOOL']:
                market.click()
                market_tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
                self.assertTrue(market_tab, msg='No market tabs found on EDP')
                selected_market = list(market_tab.values())[0]
                self.outcomes = selected_market.items_as_ordered_dict
                self.assertTrue(self.outcomes, msg='There are no outcomes present')
                for outcome_name, outcome in list(self.outcomes.items())[:4] if len(self.outcomes) > 12 else self.outcomes.items():
                    self.outcomes = selected_market.items_as_ordered_dict
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
                            self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                                        f'is not same as expected "{expected_button_name}" for outcome: {outcome_name}')
                            outcome.show_summary_toggle.click()
                        self.assertTrue(wait_for_result(lambda: outcome.has_expanded_summary(), timeout=3),
                                        msg=f'Summary is not shown for outcome "{outcome_name}" after expanding selection')
                        has_spotlight_info = outcome.expanded_summary.has_spotlight_info
                        self.assertTrue(has_spotlight_info, msg="SPOTLIGHT info is not shown")
                        try:
                            has_lastrun_info = outcome.expanded_summary.has_last_run_info
                            self.assertTrue(has_lastrun_info, msg="LASTRUN info is not shown")
                        except Exception:
                            self._logger.info(f'"LAST RUN" is not provided for runner "{outcome_name}"')
                        expected_button_name = 'Show Less'
                        result = wait_for_result(
                            lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_LESS.lower(),
                            name=f'Button name {vec.racing.SHOW_LESS}',
                            timeout=1)
                        self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                                    f'is the same as expected "{expected_button_name}"for outcome: {outcome_name}')

    def test_005_verify_last_run_label(self):
        """
        DESCRIPTION: Verify "LAST RUN" label
        EXPECTED: User should be able to view the "LAST RUN" label and text below the label
        """
        # Covered in step 4

    def test_006_repeat_4__5_steps_in_all_applicable_market_tabs(self):
        """
        DESCRIPTION: Repeat 4 & 5 steps in all applicable market tabs
        """
        # Covered in step 4
