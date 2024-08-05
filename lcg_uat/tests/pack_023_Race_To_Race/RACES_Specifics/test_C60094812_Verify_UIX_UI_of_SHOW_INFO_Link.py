import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.crl_prod
# @pytest.mark.hl
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094812_Verify_UIX_UI_of_SHOW_INFO_Link(BaseRacing):
    """
    TR_ID: C60094812
    NAME: Verify UIX/UI of "SHOW INFO" Link
    DESCRIPTION: This test case verifies  UIX/UI of "SHOW INFO" Link like CSS, Font & Style guide
    PRECONDITIONS: 1. Horse racing meeting event, should be available
    """
    keep_browser_open = True

    def test_001_launch__coral_urlfor_coral_mobile_app_launch_app(self):
        """
        DESCRIPTION: Launch  Coral URL
        DESCRIPTION: For Coral Mobile App: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: Coral App should be opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing', timeout=20)
        current_tab_name = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Default tab is "{current_tab_name}" not "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')

    def test_003_verify_any_country_panel_meeting_is_available(self):
        """
        DESCRIPTION: Verify any Country Panel meeting is available
        EXPECTED: The meetings in Country panel should be displayed
        """
        self.site.wait_splash_to_hide()
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display any section')
        found_event = False
        for section_name, section in sections.items():
            if section_name in vec.racing.COUNTRY_SKIP_LIST or self.next_races_title in section_name:
                continue
            else:
                meetings = section.items_as_ordered_dict
                self.assertTrue(meetings, msg='Failed to display any meeting')
                for meeting_name, meeting in meetings.items():
                    events = meeting.items_as_ordered_dict
                    self.assertTrue(events, msg='Failed to display any event')
                    for event_name, event in events.items():
                        race_started = event.is_resulted or event.has_race_off()
                        if not race_started:
                            event.click()
                            self.site.wait_content_state('RacingEventDetails')
                            found_event = True
                            break
                    if found_event is True:
                        break
                    else:
                        continue
                if found_event is True:
                    break
                else:
                    continue
        self.site.wait_content_state_changed()
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)

    def test_004_click_on_the_any_horse_race_meeting_event(self):
        """
        DESCRIPTION: Click on the any horse race meeting event
        EXPECTED: User should be able to navigate to event detail page. (EDP)
        """
        # Covered in Step 3

    def test_005_verify_uixui_of_show_info_link(self):
        """
        DESCRIPTION: Verify UIX/UI of "SHOW INFO" Link
        EXPECTED: .Market-Title-Copy-2 {
        EXPECTED: font-family: Lato;
        EXPECTED: font-size: 11px;
        EXPECTED: font-weight: 700;
        EXPECTED: font-stretch: normal;
        EXPECTED: color: #084d8d;
        EXPECTED: }
        """
        show_info_link = wait_for_result(lambda: self.site.racing_event_details.show_info_link, timeout=5)
        show_info_link_text = self.site.racing_event_details.show_info_link_text
        self.assertEqual(show_info_link_text.upper(), vec.racing.SHOW_INFO_TEXT.upper(),
                         msg=f'Actual link text : "{show_info_link_text}" Expected link text : "{vec.racing.SHOW_INFO_TEXT}"')
        actual_font_size = show_info_link.css_property_value('font-size')
        if self.device_type == 'mobile':
            self.assertEqual(actual_font_size, '10px', msg='show info font size is not equal to "10px", '
                                                           f'actual result "{actual_font_size}"')
        else:
            self.assertEqual(actual_font_size, '11px', msg='show info text font size is not equal to "11px", '
                                                           f'actual result "{actual_font_size}"')
        actual_font_family = show_info_link.css_property_value('font-family')
        self.assertIn('Lato', actual_font_family, msg='show info text font family is not equal to "Lato", '
                                                      f'actual result "{actual_font_family}"')

        actual_font_weight = show_info_link.css_property_value('font-weight')
        self.assertEqual(actual_font_weight, '700', msg='show info text font weight is not equal to "700", '
                                                        f'actual result "{actual_font_weight}"')

        actual_color = show_info_link.css_property_value('color')
        self.assertEqual(actual_color, vec.colors.SHOW_INFO_COLOR,
                         msg='actual color of show info text: "{actual_color}" is not equal to the expected show '
                             f'info text color:"{vec.colors.SHOW_INFO_COLOR}"')

        actual_font_stretch = show_info_link.css_property_value('font-stretch')
        self.assertEqual(actual_font_stretch, '100%', msg='show info text font weight is not equal to "100%", '
                                                          f'actual result "{actual_font_weight}"')
