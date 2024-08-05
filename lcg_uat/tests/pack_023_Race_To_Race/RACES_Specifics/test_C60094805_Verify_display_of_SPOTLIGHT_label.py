import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result, wait_for_haul
from voltron.environments import constants as vec


# @pytest.mark.tst2 Racing Post Feed will not be available everytime on qa2 & stg2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094805_Verify_display_of_SPOTLIGHT_label(BaseRacing):
    """
    TR_ID: C60094805
    NAME: Verify display of "SPOTLIGHT" label
    DESCRIPTION: Verify that User is displayed "SPOTLIGHT" label and Spotlight text below the label in Horse racing Event Details page
    PRECONDITIONS: 1: Racing post verdict should be available for the event
    PRECONDITIONS: 2: SPOTLIGHT, LAST RUN details should be available for the horse from Racing post verdict
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    market_tabs = None

    def check_empty_strings(self, league):
        """
        DESCRIPTION:  This condition ensures that the league itself is not empty
                      and also checks if all keys in the league,
                      after stripping any whitespace, are non-empty strings.
        """
        league_name = league.keys()
        return league if league and all(item.strip() for item in league_name) else False

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch the APP
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: APP should be opened
        """
        self.site.wait_content_state("homepage")

    def test_002_click_on_horse_racing_from_sports_menufor_mobile_click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile: Click on Horse racing from Sports ribbon
        EXPECTED: User should be navigated to Horse racing landing page
        """
        cms_horse_tab_name = vec.sb.HORSERACING
        cms_horse_tab_name = cms_horse_tab_name if self.device_type == 'mobile' and self.brand == 'ladbrokes' else cms_horse_tab_name.upper()
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            all_items.get(cms_horse_tab_name).link.click()
        else:
            all_items = self.site.header.sport_menu.items_as_ordered_dict
            all_items.get(cms_horse_tab_name).click()
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_racing_event_from_uk__irish_or_usa_racing_which_has_racing_post_verdict_available(self):
        """
        DESCRIPTION: Click on any racing event from UK & Irish or USA racing which has racing post verdict available
        EXPECTED: User should be navigated to Event details page
        """
        # Selects the 'MEETINGS' or 'FEATURED' tab based on the brand
        tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        tab = next((tab for name, tab in tabs.items() if (name.upper() == 'MEETINGS' and self.brand != 'bma') or (
                name.upper() == 'FEATURED' and self.brand == 'bma')), None)
        tab.click()

        # Getting a specific Meeting
        uk_irish_races = list(self.site.horse_racing.tab_content.accordions_list.get_items(
            name=vec.racing.UK_AND_IRE_TYPE_NAME.upper()).values())[0]
        self.assertTrue(uk_irish_races, msg='UK AND IRISH RACES meeting is not available in Horse Racing SLP')

        # click on the Meeting's event time
        meeting = list(uk_irish_races.get_items(number=1).values())[0]
        events = meeting.items_as_ordered_dict
        event = next(iter(events.values()))
        event.scroll_to_we()
        self.__class__.event_id = event.event_id
        event.click()
        self.site.wait_content_state(state_name='RACINGEVENTDETAILS')
        if self.site.wait_for_stream_and_bet_overlay():
            self.site.stream_and_bet_overlay.close_button.click()
        if self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()

    def test_004_scroll_to_the_selections_horses_and_click_on_show_more_link(self):
        """
        DESCRIPTION: Scroll to the Selections (Horses) and click on "SHOW MORE" link
        EXPECTED: The following information should be displayed
        EXPECTED: 1: SPOTLIGHT
        EXPECTED: 2: LAST RUN (Last 5 races info in tabular format)
        EXPECTED: "SHOW MORE" text should be replaced with "SHOW LESS" in the expanded view
        """
        self.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        for market_name, market in self.market_tabs.items():
            self.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
            if market_name not in ['FORECAST', 'TRICAST', 'TOTEPOOL',"TO FINISH","PLACE INSURANCE",'TOP FINISH']:
                market.click()
                market_tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
                self.assertTrue(market_tab, msg='No market tabs found on EDP')
                selected_market = list(market_tab.values())[0]
                self.outcomes = selected_market.items_as_ordered_dict
                self.assertTrue(self.outcomes, msg='There are no outcomes present')
                for outcome_name, outcome in list(self.outcomes.items())[:4] if len(
                        self.outcomes) > 12 else self.outcomes.items():
                    self.outcomes = selected_market.items_as_ordered_dict
                    outcome.scroll_to()
                    if 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                        self.assertTrue(outcome.has_show_summary_toggle(),
                                        msg=f'Show more button is not present for "{outcome_name}"')
                        if outcome.toggle_icon_name.lower() != vec.racing.SHOW_LESS.lower():
                            expected_button_name = 'Show More'
                            result = wait_for_result(
                                lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_MORE.lower(),
                                name=f'Button name {vec.racing.SHOW_MORE}', timeout=1)
                            self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                                        f'is not same as expected "{expected_button_name}" for outcome: {outcome_name}')
                            outcome.show_summary_toggle.click()
                        self.assertTrue(wait_for_result(lambda: outcome.has_expanded_summary(), timeout=5),
                                        msg=f'Summary is not shown for outcome "{outcome_name}" after expanding selection')
                        spotlight_label = wait_for_result(lambda: outcome.spotlight_overview.title, timeout=5)
                        self.assertEqual(spotlight_label, vec.racing.SPOTLIGHT_TITLE.upper(),
                                         msg=f'Actual text is "{spotlight_label}" is not equal to the '
                                             f'Expected text"{vec.racing.SPOTLIGHT_TITLE.upper()}"')
                        has_spotlight_info = outcome.spotlight_overview.has_summary_text
                        self.assertTrue(has_spotlight_info, msg="SPOTLIGHT info is not shown")
                        try:
                            has_lastrun_info = outcome.expanded_summary.has_last_run_table_info
                            self.assertTrue(has_lastrun_info, msg="LASTRUN table info is not shown")
                        except Exception:
                            self._logger.info(f'"LAST RUN" is not provided for runner "{outcome_name}"')
                        expected_button_name = 'Show Less'
                        result = wait_for_result(
                            lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_LESS.lower(),
                            name=f'Button name {vec.racing.SHOW_LESS}',
                            timeout=1)
                        self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                                    f'is the same as expected "{expected_button_name}"for outcome: {outcome_name}')

    def test_005_verify_spotlight_label(self):
        """
        DESCRIPTION: Verify "SPOTLIGHT" label
        EXPECTED: "SPOTLIGHT" label should be displayed
        """
        # Covered in step 4

    def test_006_validate_the_spotlight_text(self):
        """
        DESCRIPTION: Validate the "SPOTLIGHT" text
        EXPECTED: The text should be displayed under the label
        """
        # Covered in step 4

    def test_007_repeat_4_5__6_steps_in_all_market_tabs_applicable(self):
        """
        DESCRIPTION: Repeat 4 ,5 & 6 steps in all market tabs (applicable)
        """
        # Covered in step 4
