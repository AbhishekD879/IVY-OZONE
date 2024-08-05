import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.races
@vtest
class Test_C60094810_Verify_CSSSHOW_MORESPOTLIGHTLAST_RUN_LAST_RACES_TABLE(BaseRacing):
    """
    TR_ID: C60094810
    NAME: Verify CSS:"SHOW MORE",SPOTLIGHT,LAST RUN, LAST RACES TABLE
    DESCRIPTION: Verify the CSS for  "LAST RUN" and Last 5 races information in table
    PRECONDITIONS: 1: Racing Post Verdict should be available for the event
    PRECONDITIONS: 2: SPOTLIGHT and Last Race information should be available for the Horses
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def check_empty_strings(self, list):
        """
        DESCRIPTION:  This condition ensures that the list itself is not empty
                      and also checks if all items in the list, after stripping any whitespace,
                      are non-empty strings.
        """
        return list if all(list) and all(item.strip() for item in list) else False

    def test_001_launch_ladbrokescoral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: Ladbrokes/Coral URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.__class__.cms_horse_tab_name = self.get_sport_title(category_id=21)
        self.site.wait_content_state('Homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        cms_horse_tab_name = self.cms_horse_tab_name if self.device_type == 'mobile' and self.brand == 'ladbrokes' else self.cms_horse_tab_name.upper()
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            all_items.get(cms_horse_tab_name).link.click()
        else:
            all_items = self.site.header.sport_menu.items_as_ordered_dict
            all_items.get(cms_horse_tab_name).click()
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_horse_race_event_from_uk__irish_races(self):
        """
        DESCRIPTION: Click on any Horse race event from UK / Irish races
        EXPECTED: User should be navigated to Event details page
        """
        # Selects the 'MEETINGS' or 'FEATURED' tab based on the brand
        tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        tab = next((tab for name, tab in tabs.items() if (name.upper() == 'MEETINGS' and self.brand != 'bma') or (
                name.upper() == 'FEATURED' and self.brand == 'bma')), None)
        tab.click()
        # Getting a specific Meeting
        sections = wait_for_result(lambda: self.check_empty_strings(
            self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict),
                                   name='sections list is not loaded',
                                   timeout=20)
        uk_irish_races = next(
            (ele for item, ele in sections.items() if item.upper() == vec.racing.UK_AND_IRE_TYPE_NAME.upper()), None)
        self.assertTrue(uk_irish_races, msg='UK AND IRISH RACES meeting is not available in Horse Racing SLP')

        # click on the Meeting's event time
        meetings = wait_for_result(lambda: list(uk_irish_races.items_as_ordered_dict.values()), timeout=10)
        self.__class__.meetings_length = len(meetings)
        meeting = meetings[0]
        events = meeting.items_as_ordered_dict
        event = next(iter(events.values()))
        event.scroll_to_we()
        event.click()
        self.site.wait_content_state(state_name='RACINGEVENTDETAILS')
        self.site.wait_content_state_changed(timeout=5)
        current_market_tab = self.site.racing_event_details.tab_content.event_markets_list.current_market_tab_name
        if current_market_tab != vec.racing.RACING_EDP_MARKET_TABS.win_or_ew:
            market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
            if vec.racing.RACING_EDP_MARKET_TABS.win_or_ew in market_tabs.keys():
                market_tabs[vec.racing.RACING_EDP_MARKET_TABS.win_or_ew].click()
                self.site.wait_content_state_changed(timeout=5)

    def test_004_scroll_to_the_selections_horses_and_click_on_show_more_link(self):
        """
        DESCRIPTION: Scroll to the Selections (Horses) and click on "SHOW MORE" link
        EXPECTED: The following information should be displayed
        EXPECTED: 1: SPOTLIGHT
        EXPECTED: 2: LAST RUN
        EXPECTED: "SHOW MORE" text should be replaced with "SHOW LESS" in the expanded view
        """
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        for item in ['FORECAST', 'TRICAST', 'TOTEPOOL']:
            if item in market_tabs.keys():
                del market_tabs[item]
        self.assertTrue(market_tabs, msg='No market tabs found on EDP')
        market = list(market_tabs.values())[0]
        self.assertTrue(market, msg='No market tabs found on EDP')
        market.click()
        market_tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(market_tab, msg='No market tabs found on EDP')
        selected_market = list(market_tab.values())[0]
        self.outcomes = selected_market.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No one outcome was found in section: "%s"' % selected_market)
        self.assertTrue(self.outcomes, msg='There are no outcomes present')
        for outcome_name, outcome in list(self.outcomes.items())[:4] if len(
                self.outcomes) > 4 else self.outcomes.items():
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
                    self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_MORE}" '
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
                # CSS verification for Last run label
                lastrun_info = wait_for_result(lambda: outcome.expanded_summary.has_last_run_info, timeout=20,
                                               name='Last run info to be displayed')
                if not lastrun_info:
                    continue
                lastrun_info_label = outcome.expanded_summary.last_run_info_label
                actual_font_size = lastrun_info_label.css_property_value('font-size')
                self.assertEqual(actual_font_size, '12px',
                                 msg=f'Last run font size is not equal to "12px", actual result: "{actual_font_size}"')
                actual_font_family = lastrun_info_label.css_property_value('font-family')
                self.assertIn('Helvetica Neue', actual_font_family,
                              msg=f'Last run font family is not equal to "Helvetica Neue", actual result "{actual_font_family}"')
                actual_font_weight = lastrun_info_label.css_property_value('font-weight')
                self.assertEqual(actual_font_weight, '700', msg='Last run font weight is not equal to "700", '
                                                                f'actual result "{actual_font_weight}"')
                actual_color = lastrun_info_label.css_property_value('color')
                self.assertEqual(actual_color, vec.colors.COMPLIANCE_INFO_FONT_COLOR_GREY if self.brand == 'bma' else vec.colors.LADBROKES_COMPLIANCE_INFO_FONT_COLOR,
                                 msg=f'actual color of Last run: "{actual_color}" is not equal to the expected Last run'
                                     f' color:"{vec.colors.COMPLIANCE_INFO_FONT_COLOR_GREY if self.brand == "bma" else vec.colors.LADBROKES_COMPLIANCE_INFO_FONT_COLOR}"')
                # CSS verification for Last run text
                lastrun_info_text = outcome.expanded_summary.last_run_info_text
                actual_font_size = lastrun_info_text.css_property_value('font-size')
                self.assertEqual(actual_font_size, '12px',
                                 msg=f'Last run font size is not equal to "12px", actual result: "{actual_font_size}"')
                actual_font_family = lastrun_info_text.css_property_value('font-family')
                self.assertIn('Helvetica Neue'if self.brand == 'bma'else 'Roboto Condensed', actual_font_family,
                              msg=f'Last run font family is not equal to "Helvetica Neue", actual result "{actual_font_family}"')
                actual_font_weight = lastrun_info_text.css_property_value('font-weight')
                self.assertEqual(actual_font_weight, '400', msg='Last run font weight is not equal to "400", '
                                                                f'actual result "{actual_font_weight}"')
                actual_color = lastrun_info_text.css_property_value('color')
                self.assertEqual(actual_color, vec.colors.COMPLIANCE_INFO_FONT_COLOR_GREY if self.brand == 'bma' else vec.colors.LADBROKES_COMPLIANCE_INFO_FONT_COLOR,
                                 msg=f'actual color of Last run: "{actual_color}" is not equal to the expected Last run'
                                     f'color:"{vec.colors.COMPLIANCE_INFO_FONT_COLOR_GREY if self.brand == "bma" else vec.colors.LADBROKES_COMPLIANCE_INFO_FONT_COLOR}"')
                # CSS verification for Last run table
                is_table = outcome.expanded_summary.has_last_run_table_info
                self.assertTrue(is_table, msg='Last run info table was not found')
                table_header = outcome.expanded_summary.last_run_table_header_info
                actual_font_size = table_header.css_property_value('font-size')
                self.assertEqual(actual_font_size, '9px',
                                 msg=f'Last run table data font size is not equal to "9px", actual result: "{actual_font_size}"')
                actual_font_family = table_header.css_property_value('font-family')
                self.assertIn("Helvetica Neue", actual_font_family,
                              msg=f'Last run table data font family is not equal to "Helvetica Neue", actual result "{actual_font_family}"')
                actual_font_weight = table_header.css_property_value('font-weight')
                self.assertEqual(actual_font_weight, '400', msg='Last run table data font weight is not equal to "400",'
                                                                f' actual result "{actual_font_weight}"')
                actual_color = table_header.css_property_value('color')
                if self.brand == 'bma' and self.device_type in ['mobile', 'tablet']:
                    expected_color = vec.colors.LAST_RUN_TABLE_TEXT_COLOR
                elif self.brand == 'bma':
                    expected_color = vec.colors.COMPLIANCE_INFO_FONT_COLOR_GREY
                else:
                    expected_color = vec.colors.LADBROKES_COMPLIANCE_INFO_FONT_COLOR
                self.assertEqual(actual_color, expected_color,
                                 msg=f'actual color of Last run table data: "{actual_color}" is not equal to the '
                                     f'expected Last run color:"{expected_color}"')
                table_data = outcome.expanded_summary.last_run_table_data_info
                actual_font_size = table_data.css_property_value('font-size')
                self.assertEqual(actual_font_size, '9px',
                                 msg=f'Last run table data font size is not equal to "9px", actual result: "{actual_font_size}"')
                actual_font_family = table_data.css_property_value('font-family')
                self.assertIn("Helvetica Neue", actual_font_family,
                              msg=f'Last run table data font family is not equal to "Helvetica Neue", actual result "{actual_font_family}"')
                actual_font_weight = table_data.css_property_value('font-weight')
                self.assertEqual(actual_font_weight, '400', msg='Last run table data font weight is not equal to "400",'
                                                                f' actual result "{actual_font_weight}"')
                actual_color = table_data.css_property_value('color')
                self.assertEqual(actual_color, expected_color,
                                 msg=f'actual color of Last run table data: "{actual_color}" is not equal to the '
                                     f'expected Last run table data color:"{expected_color}"')

    def test_005_verify_the_css_for_the_last_run_label_and_text(self):
        """
        DESCRIPTION: Verify the CSS for the Last Run label and text
        EXPECTED: The last run lable css should be:
        EXPECTED: .LAST-RUN {
        EXPECTED: width: 64px;
        EXPECTED: height: 19px;
        EXPECTED: font-family: HelveticaNeue;
        EXPECTED: font-size: 11px;
        EXPECTED: font-weight: bold;
        EXPECTED: font-stretch: normal;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: -0.27px;
        EXPECTED: color: #2b2b2b;
        EXPECTED: and the text CSS should be:
        EXPECTED: .-\39 -7-Chased-le {
        EXPECTED: width: 351px;
        EXPECTED: height: 42px;
        EXPECTED: font-family: Helvetica;
        EXPECTED: font-size: 12px;
        EXPECTED: font-weight: normal;
        EXPECTED: font-stretch: normal;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: -0.29px;
        EXPECTED: color: #2b2b2b;
        }
        """
        # Covered in the step test_004

    def test_006_verifies_the_css_for_the_last_races_table(self):
        """
        DESCRIPTION: Verifies the CSS for the Last races table
        EXPECTED: As per the Design
        """
        # Covered in the step test_004
