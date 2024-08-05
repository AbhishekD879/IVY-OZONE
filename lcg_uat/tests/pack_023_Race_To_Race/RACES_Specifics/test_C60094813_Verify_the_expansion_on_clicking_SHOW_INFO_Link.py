import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@vtest
class Test_C60094813_Verify_the_expansion_on_clicking_SHOW_INFO_Link(BaseRacing):
    """
    TR_ID: C60094813
    NAME: Verify the expansion on clicking "SHOW INFO" Link
    DESCRIPTION: This Test case describes  the expansion of panels for all the horses related information in that meeting point is displayed on clicking "SHOW INFO" Link
    PRECONDITIONS: 1. Horse racing meeting events, should be available
    """
    keep_browser_open = True

    def test_001_launch__coral_urlfor_coral_mobile_app_launch_app(self):
        """
        DESCRIPTION: Launch  Coral URL
        DESCRIPTION: For Coral Mobile App: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: Coral App should be opened
        """
        # Covered in Step 2

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        try:
            cms_horse_tab_name = self.get_sport_title(category_id=self.ob_config.horseracing_config.category_id)
            if self.device_type == 'desktop':
                self.site.header.sport_menu.items_as_ordered_dict.get(cms_horse_tab_name.upper()).click()
            else:
                if self.brand == 'ladbrokes':
                    self.site.home.menu_carousel.items_as_ordered_dict.get(cms_horse_tab_name).click()
                else:
                    self.site.home.menu_carousel.items_as_ordered_dict.get(cms_horse_tab_name.upper()).click()
            self.site.wait_content_state(state_name='horse-racing')
        except Exception as e:
            self._logger.warning(e)
            self.navigate_to_page('horse-racing')

    def test_003_verify_any_country_panel_meeting_is_available(self):
        """
        DESCRIPTION: Verify any Country Panel meeting is available
        EXPECTED: The meetings in Country panel should be displayed
        """
        self.site.wait_splash_to_hide(timeout=60)
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
                            self.site.wait_splash_to_hide()
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

    def test_004_click_on_the_any_horse_race_meeting_event(self):
        """
        DESCRIPTION: Click on the any horse race meeting event
        EXPECTED: User should be able to navigate to event detail page. (EDP)
        """
        # Covered in Step 3

    def test_005_verify__expansion_of_panels_for_all_the_horses_related_information_in_that_meeting_point_is_displayed_on_clicking_show_info_link(self):
        """
        DESCRIPTION: Verify  expansion of panels for all the horses related information in that meeting point is displayed on clicking "SHOW INFO" Link
        EXPECTED: User should able to see the expansion of panels for all the horses related information.
        """
        self.market_tabs = \
            self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        for market_name, market in self.market_tabs.items():
            if market_name not in ['FORECAST', 'TRICAST', 'TOTEPOOL']:
                market.click()
                break
        sleep(2)
        racing_details = self.site.racing_event_details
        link_text = racing_details.show_info_link_text
        self.assertEqual(link_text.upper(), vec.racing.SHOW_INFO_TEXT.upper(),
                         msg=f'Actual link text : "{link_text}" Expected link text : "{vec.racing.SHOW_INFO_TEXT}"')
        racing_details.show_info_link.click()
        wait_for_result(
            lambda: self.site.racing_event_details.show_info_link_text == vec.racing.HIDE_INFO_TEXT.upper(),
            name='Wait for Hide info link to display',
            timeout=10)
        self.assertEqual(self.site.racing_event_details.show_info_link_text.upper(), vec.racing.HIDE_INFO_TEXT.upper(),
                         msg=f'Actual link text : "{self.site.racing_event_details.show_info_link_text}" '
                             f'Expected link text : "{vec.racing.HIDE_INFO_TEXT}"')

        market_tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(market_tab, msg='No market tabs found on EDP')
        selected_market = list(market_tab.values())[0]
        self.outcomes = selected_market.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='There are no outcomes present')
        for outcome_name, outcome in list(self.outcomes.items())[:4] if len(
                self.outcomes) > 12 else self.outcomes.items():
            outcome.scroll_to()
            if 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                self.assertTrue(outcome.has_expanded_summary(), msg=f'The outcome "{outcome_name}" is not expanded')
