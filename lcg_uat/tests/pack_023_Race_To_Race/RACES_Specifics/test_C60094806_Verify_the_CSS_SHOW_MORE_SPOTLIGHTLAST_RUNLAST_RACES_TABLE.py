import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2  Feed will not be available on qa2 & stg2
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@vtest
class Test_C60094806_Verify_the_CSS_SHOW_MORE_SPOTLIGHTLAST_RUNLAST_RACES_TABLE(BaseRacing):
    """
    TR_ID: C60094806
    NAME: Verify the CSS "SHOW MORE", SPOTLIGHT,LAST RUN,LAST RACES TABLE
    DESCRIPTION: Verify the CSS for "SHOW MORE" link, "SPOTLIGHT"
    PRECONDITIONS: 1: Racing Post Verdict should be available for the event
    PRECONDITIONS: 2: SPOTLIGHT and Last Race information should be available for the Horses
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
        self.site.wait_content_state('Homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        sport = 'Horse Racing' if self.brand != 'bma' and self.device_type == 'mobile' else 'HORSE RACING'
        if self.device_type == 'desktop':
            self.site.sport_menu.click_item(sport)
        else:
            self.navigate_to_page('horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_003_click_on_any_horse_race_event_from_uk__irish_races(self):
        """
        DESCRIPTION: Click on any Horse race event from UK / Irish races
        EXPECTED: User should be navigated to Event details page
        """
        self.site.wait_splash_to_hide()
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict.get(self.uk_and_ire_type_name)
        self.assertTrue(sections, msg='No sections found for UK & IRE country')
        expected_event = None
        expected_meeting_name = None
        meetings = sections.items_as_ordered_dict
        for meeting_name, meeting in meetings.items():
            events = meeting.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events found for meeting name "{meeting_name}"')
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
        actual_meeting_name = self.site.racing_event_details.tab_content.race_details.event_title.strip()
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
        for mrkt_name, mrkt_value in self.market_tabs.items():
            if mrkt_name not in ['FORECAST', 'TRICAST', 'TOTEPOOL']:
                mrkt_value.click()
                break
        market_tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(market_tab, msg='No market tabs found on EDP')
        selected_market = list(market_tab.values())[0]
        self.outcomes = selected_market.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='There are no outcomes present')
        for outcome_name, outcome in list(self.outcomes.items())[:4] if len(self.outcomes) > 12 else self.outcomes.items():
            self.outcomes = selected_market.items_as_ordered_dict
            outcome.scroll_to()
            if 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                result = wait_for_result(
                    lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_MORE.lower(),
                    name=f'Button name {vec.racing.SHOW_MORE}',
                    timeout=2)
                self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_MORE}" is not shown for outcome: {outcome_name}')
                actual_font_size = outcome.show_summary_toggle.css_property_value('font-size')
                expected_font_size = '9px' if self.brand == 'bma' else '11px'
                self.assertEqual(actual_font_size, expected_font_size,
                                 msg=f'SHOW MORE font size is not equal to "{expected_font_size}", actual result: "{actual_font_size}"')
                actual_font_family = outcome.show_summary_toggle.css_property_value('font-family')
                expected_font_family = 'Lato' if self.brand == 'bma' else 'Roboto'
                self.assertIn(expected_font_family, actual_font_family,
                              msg=f'SHOW MORE font family is not equal to "{expected_font_family}", actual result "{actual_font_family}"')
                # show more css
                actual_font_weight = outcome.show_summary_toggle.css_property_value('font-weight')
                self.assertEqual(actual_font_weight, '700', msg='SHOW MORE font weight is not equal to "700" '
                                                                'actual result "{actual_font_weight}"')
                actual_color = outcome.show_summary_toggle.css_property_value('color')
                self.assertEqual(actual_color, vec.colors.SHOW_INFO_COLOR,
                                 msg=f'actual color of SHOW MORE: "{actual_color}" is not equal to the expected SHOW MORE '
                                     f'color:"{vec.colors.SHOW_INFO_COLOR if self.brand == "bma" else vec.colors.RACE_OFF_COLOR}"')
                outcome.show_summary_toggle.click()
                self.assertTrue(wait_for_result(lambda: outcome.has_expanded_summary(), timeout=3),
                                msg=f'Summary is not shown for outcome "{outcome_name}" after expanding selection')
                has_spotlight_info = outcome.expanded_summary.has_spotlight_info
                self.assertTrue(has_spotlight_info, msg="SPOTLIGHT info is not shown")

                # spotlight title css
                actual_font_size = outcome.spotlight_overview.spotlight_title.css_property_value('font-size')
                self.assertEqual(actual_font_size, '12px', msg=f'SPOTLIGHT TITLE font size is not equal to "9px", '
                                                               f'actual result: "{actual_font_size}"')
                actual_font_family = outcome.spotlight_overview.spotlight_title.css_property_value('font-family')
                self.assertIn('Helvetica', actual_font_family,
                              msg=f'SPOTLIGHT TITLE font family is not equal to "Helvetica", actual result "{actual_font_family}"')
                actual_font_weight = outcome.spotlight_overview.spotlight_title.css_property_value('font-weight')
                self.assertEqual(actual_font_weight, '700', msg='SPOTLIGHT TITLE font weight is not equal to "700" '
                                                                'actual result "{actual_font_weight}"')
                actual_color = outcome.spotlight_overview.spotlight_title.css_property_value('color')
                expected_color = vec.colors.COMPLIANCE_INFO_FONT_COLOR_GREY if self.brand == 'bma' else vec.colors.LADBROKES_COMPLIANCE_INFO_FONT_COLOR
                self.assertEqual(actual_color, expected_color, msg=f'actual color of SPOTLIGHT TITLE: "{actual_color}" '
                                                                   f'is not equal to the expected color:"{expected_color}"')
                # spotlight text css
                actual_font_size = outcome.spotlight_overview.summary_text.css_property_value('font-size')
                self.assertEqual(actual_font_size, '12px',
                                 msg=f'SPOTLIGHT TEXT font size is not equal to "12px", actual result: "{actual_font_size}"')
                actual_font_family = outcome.spotlight_overview.summary_text.css_property_value('font-family')
                expected_font_family1 = 'Helvetica' if self.brand == 'bma' else 'Roboto'
                self.assertIn(expected_font_family1, actual_font_family,
                              msg=f'SPOTLIGHT TEXT font family is not equal to "{expected_font_family1}", actual result "{actual_font_family}"')
                actual_font_weight = outcome.spotlight_overview.summary_text.css_property_value('font-weight')
                self.assertEqual(actual_font_weight, '400', msg=f'SPOTLIGHT TEXT font weight is not equal to "400" '
                                                                f'actual result "{actual_font_weight}"')
                actual_color = outcome.spotlight_overview.summary_text.css_property_value('color')
                self.assertEqual(actual_color, expected_color,
                                 msg=f'actual color of SPOTLIGHT TEXT: "{actual_color}" is not equal to the expected "{expected_color}" ')

                # Show less css
                result = wait_for_result(
                    lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_LESS.lower(), name=f'Button name {vec.racing.SHOW_LESS}',
                    timeout=1)
                self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" is NOT shown for outcome: {outcome_name}')
                actual_font_size = outcome.show_summary_toggle.css_property_value('font-size')
                self.assertEqual(actual_font_size, expected_font_size, msg=f'SHOW LESS font size is not equal to "{expected_font_size}", '
                                                                           f'actual result: "{actual_font_size}"')
                actual_font_family = outcome.show_summary_toggle.css_property_value('font-family')
                self.assertIn(expected_font_family, actual_font_family, msg=f'SHOW LESS font family is not equal to "{expected_font_family}", '
                                                                            f'actual result "{actual_font_family}"')
                actual_font_weight = outcome.show_summary_toggle.css_property_value('font-weight')
                self.assertEqual(actual_font_weight, '700', msg='Race off font weight is not equal to "700" '
                                                                'actual result "{actual_font_weight}"')
                actual_color = outcome.show_summary_toggle.css_property_value('color')
                self.assertEqual(actual_color, vec.colors.SHOW_INFO_COLOR,
                                 msg=f'actual color of Race off: "{actual_color}" is not equal to the expected Race off '
                                     f'color:"{vec.colors.SHOW_INFO_COLOR if self.brand == "bma" else vec.colors.RACE_OFF_COLOR}"')

    def test_005_verify_the_css_for_the_show_more_link(self):
        """
        DESCRIPTION: Verify the CSS for the Show more link
        EXPECTED: The css should be
        EXPECTED: .SHOW-MORE {
        EXPECTED: width: 56px;
        EXPECTED: height: 15px;
        EXPECTED: font-family: Roboto;
        EXPECTED: font-size: 11px;
        EXPECTED: font-weight: bold;
        EXPECTED: font-stretch: condensed;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: 0px;
        EXPECTED: text-align: right;
        EXPECTED: color: #4a90e2;
        EXPECTED: }
        """
        # Covered in step 4

    def test_006_verify_the_css_for_the_show_less_link(self):
        """
        DESCRIPTION: Verify the CSS for the Show less link
        EXPECTED: The css should be
        EXPECTED: .SHOW-LESS {
        EXPECTED: width: 53px;
        EXPECTED: height: 15px;
        EXPECTED: font-family: Roboto;
        EXPECTED: font-size: 11px;
        EXPECTED: font-weight: bold;
        EXPECTED: font-stretch: condensed;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: 0px;
        EXPECTED: text-align: right;
        EXPECTED: color: #4a90e2;
        EXPECTED: }
        """
        # Covered in step 4

    def test_007_verify_the_css_for_the_spotlight_label_and_text(self):
        """
        DESCRIPTION: Verify the CSS for the Spotlight label and text
        EXPECTED: The lable css should be
        EXPECTED: width: 61px;
        EXPECTED: height: 13px;
        EXPECTED: font-family: HelveticaNeue;
        EXPECTED: font-size: 11px;
        EXPECTED: font-weight: bold;
        EXPECTED: letter-spacing: -0.27px;
        EXPECTED: color: #2b2b2b;
        EXPECTED: And the text css should be:
        EXPECTED: .Popped-up-in-a-Plump {
        EXPECTED: width: 293px;
        EXPECTED: height: 70px;
        EXPECTED: font-family: Helvetica;
        EXPECTED: font-size: 12px;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: normal;
        """
        # Covered in step 4
