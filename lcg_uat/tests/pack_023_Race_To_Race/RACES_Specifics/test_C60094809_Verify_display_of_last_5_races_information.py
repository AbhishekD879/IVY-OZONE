import pytest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


# @pytest.mark.tst2 Feed will not be available
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@vtest
class Test_C60094809_Verify_display_of_last_5_races_information(BaseRacing):
    """
    TR_ID: C60094809
    NAME: Verify display of last 5 races information
    DESCRIPTION: Verify that Last 5 races information is displayed in a tabular format under the LAST RUN label
    PRECONDITIONS: 1: Racing Post Verdict should be available for the event
    PRECONDITIONS: 2: SPOTLIGHT and Last Race information should be available for the Horses
    """
    keep_browser_open = True
    expected_last_run_table_headers_mobile = ['Date', 'Conditions', 'Weight', 'Analysis', 'RPR', 'OR']
    expected_last_run_table_headers_desktop = ['Date', 'Conditions', 'Weight', 'Analysis', 'Jockey', 'OR', 'TS', 'RPR']

    def test_001_launch_ladbrokescoral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: Ladbrokes/Coral URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        # Covered in step 3

    def test_003_click_on_any_horse_race_event_from_uk__irish_races(self):
        """
        DESCRIPTION: Click on any Horse race event from UK / Irish races
        EXPECTED: User should be navigated to Event details page
        """
        event_info = self.get_event_details(race_form_info=True, racing_post_verdict=True, df_event_summary=True)
        self.__class__.event_id = event_info.event_id
        self.__class__.horse_details = event_info.datafabric_data['horses']
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')

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
        expected_last_race_headers = self.expected_last_run_table_headers_mobile if self.device_type == 'mobile' else self.expected_last_run_table_headers_desktop
        for market_name, market in list(self.market_tabs.items())[:4] if len(self.market_tabs) > 5 else self.market_tabs.items():
            self.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
            if market_name not in ['FORECAST', 'TRICAST', 'TOTEPOOL']:
                market.click()
                self.site.racing_event_details.tab_content.choose_sorting_option(option=vec.racing.CARD_SORTING_OPTION)
                market_tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
                self.assertTrue(market_tab, msg='No market tabs found on EDP')
                selected_market = list(market_tab.values())[0]
                self.outcomes = selected_market.items_as_ordered_dict
                self.assertTrue(self.outcomes, msg='There are no outcomes present')
                horse_index = 0
                for outcome_name, outcome in list(self.outcomes.items())[:4] if len(
                        self.outcomes) > 6 else self.outcomes.items():
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
                        expected_button_name = 'Show Less'
                        result = wait_for_result(
                            lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_LESS.lower(),
                            name=f'Button name {vec.racing.SHOW_LESS}',
                            timeout=3)
                        self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                                    f'is the same as expected "{expected_button_name}"for outcome: {outcome_name}')
                        has_lastrun_info = wait_for_result(lambda: outcome.expanded_summary.has_last_run_info,
                                                           timeout=3)
                        if has_lastrun_info:
                            actual_last_races_num = outcome.expanded_summary.last_run_item_details
                            expected_last_races_num = self.horse_details[horse_index]['form']
                            self.assertLessEqual(len(actual_last_races_num) - 1, len(expected_last_races_num),
                                                 msg=f'Actual last races number "{len(actual_last_races_num)-1}" '
                                                 f'is NOT same as expected "{len(expected_last_races_num)}"')
                            actual_last_run_table_headers = outcome.expanded_summary.last_run_item_details[0].text.split(" ")
                            self.assertEqual(actual_last_run_table_headers, expected_last_race_headers,
                                             msg=f'Actual headers "{actual_last_run_table_headers}" is not same as expected "{expected_last_race_headers}" ')
                        horse_index = horse_index + 1

    def test_005_verify_the_last_5_races_information_under_last_run_label(self):
        """
        DESCRIPTION: Verify the Last 5 races information under LAST RUN label
        EXPECTED: User should be displayed Last 5 races information under LAST RUN label.
        EXPECTED: Last 5 races information should be displayed in a tabular format with below Column headers,
        EXPECTED: 1: Date
        EXPECTED: 2: Conditions
        EXPECTED: 3: Weight
        EXPECTED: 4; Analysis
        EXPECTED: 5: Jockey
        EXPECTED: 6: RPR
        EXPECTED: 7: OR
        """
        # Covered in Step 04

    def test_006_repeat_4__5_steps_in_all_market_tabs(self):
        """
        DESCRIPTION: Repeat 4 & 5 steps in all market tabs
        EXPECTED:
        """
        # Covered in Step 04
